from __future__ import annotations
import base64
import re
import sys
import typing
import zlib
from pathlib import Path
from textwrap import dedent
from dataclasses import dataclass

HERE = Path(__file__).parent.resolve()
DERIVEDAGES = HERE.joinpath("DerivedAge.txt")

@dataclass
class Span:
    start: int
    stop: int
    major: int
    minor: int

def _encode(b: bytes) -> str:
    zb = zlib.compress(b, 9)
    a85 = base64.a85encode(zb, wrapcol=78).decode("ascii")
    # Very unlikely sequence (1 in 614125) must be changed to not look like an end triple quote
    # in a way that is still a85-decodable
    while "'''" in a85:
        a85 = a85.replace("'''", "' ''")
    return a85

def _write_spans(spans: list[Span], version_map: dict[tuple[int, int], int], ucd_version: tuple[int, ...], outfile: Path):
    version_reverse = [None] * len(version_map)
    for k, v in version_map.items():
        version_reverse[v-1] = k

    counts = []
    versions = []
    def add_span(n, v):
        c = n - 1
        # Avoid a span whose length corresponds to a UTF-16 surrogate, as these
        # values are not permitted to be encoded in UTF-8.
        # This will recurse at most once.
        # The decoder need not know about this little quirk.
        # As of the Unicode standard 18.0 there are no such spans so this is untested.
        if 0xd800 <= c < 0xdfff:
            add_span(0xd800, v)
            c -= 0xd800
        counts.append(c)
        versions.append(v)

    last = 0
    for s in spans:
        if s.start > last:
            add_span(s.start-last, 0)
        add_span(s.stop - s.start + 1, version_map[s.major, s.minor])
        last = s.stop + 1

    vbuf = _encode(bytes(versions))
    cbuf = _encode("".join(chr(c) for c in counts).encode("utf-8"))

    py_src = dedent("""\
    # Generated file, do not edit
    import zlib
    import base64

    UCD_VERSION = {ucd_version}

    version_map = {version_reverse!r}

    def iter_spans():
        start = 0
        for count, packed_ver in zip(_counts, _versions):
            stop = start + ord(count)
            if packed_ver:
                yield (start, stop, *version_map[packed_ver-1])
            start = stop + 1

    _versions = zlib.decompress(base64.a85decode(rb'''
    {vbuf}
    '''))

    _counts = zlib.decompress(base64.a85decode(rb'''
    {cbuf}\
    ''')).decode("utf-8")

    """).format(ucd_version=ucd_version, vbuf=vbuf, cbuf=cbuf, version_reverse=version_reverse)


    outfile.write_text(py_src)
    print(f"Wrote {outfile.stat().st_size} bytes to {outfile}")


def _merge_spans(spans: typing.Iterator[Span]) -> typing.Generator[Span]:
    last = next(spans) 
    merged = 0
    for span in spans:
        assert span.start > last.stop
        if span.major == last.major and span.minor == last.minor and span.start == last.stop + 1:
            last.stop = span.stop
            merged = merged + 1
        else:
            yield last
            last = span
    print(f"Merged {merged} spans")
    yield last

def _derivedage_spans(fn: Path) -> typing.Generator[Span]:
    CODEPT = r"[0-9A-Fa-f]+"
    PATT = rf"^({CODEPT})(?:\.\.({CODEPT}))?\s*;\s*([\d.]+)\s*#.*"

    with open(fn, "r") as f:
        for line in f:
            if line.strip() and line.startswith("#"):
                continue
            if m := re.match(PATT, line):
                start, stop, ver = m.groups()
                start = int(start, base=16)
                if stop:
                    stop = int(stop, base=16)
                    stop = min(stop, sys.maxunicode)
                else:
                    stop = start

                major, minor = [int(part) for part in ver.split('.')]

                yield Span(start, stop, major, minor)


def parse_ucdversion(fn: Path) -> tuple[int, ...]:
    with open(fn, "r") as f:
        patt = r"DerivedAge-(?P<version>\d+\.\d+\.\d+)\.txt"
        m = re.search(patt, f.readline())
        if not m:
            raise ValueError("Cannot determine UCD version of {str(fn)!r}")

    ver = tuple(int(val) for val in m.group("version").split('.'))
    return ver


def main():
    ucd_version = parse_ucdversion(DERIVEDAGES)
    print(f"Scanning for version spans for UCD {ucd_version}: {str(DERIVEDAGES)}")
    spans = _derivedage_spans(DERIVEDAGES)
    spans = sorted(spans, key=lambda x: x.start)
    spans = list(_merge_spans(iter(spans)))
    print(f"Found {len(spans)} versioned spans")

    UNICODE_AGE = HERE.joinpath("src", "unicode_age")
    PYTHON_OUTFILE = UNICODE_AGE.joinpath("unicode_age_db.py")

    all_ages = sorted(set((s.major, s.minor) for s in spans))
    assert len(all_ages) < 256
    version_map = {si: i+1 for i, si in enumerate(all_ages)}
    _write_spans(
        spans,
        version_map,
        ucd_version=ucd_version,
        outfile=PYTHON_OUTFILE,
    )


if __name__ == "__main__":
    main()
