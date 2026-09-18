from __future__ import annotations
import binascii
import re
import struct
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

def _write_spans(spans: list[Span], ucd_version: tuple[int, ...], outfile: Path):
    span_fmt = "iibb"
    VersionSpan = struct.Struct(span_fmt)

    Nbytes = len(spans) * VersionSpan.size
    buf = bytearray(Nbytes)

    for n, s in enumerate(spans):
        VersionSpan.pack_into(buf, n*VersionSpan.size, s.start, s.stop, s.major, s.minor)

    zbuf = zlib.compress(buf, 9)
    b64buf = binascii.b2a_base64(zbuf, newline=False)
    n = 64
    b64rows = "\n".join(repr(b64buf[i:i+n]) for i in range(0, len(b64buf), n))

    py_src = dedent("""
    from __future__ import annotations
    import struct
    import zlib
    import binascii

    UCD_VERSION = {ucd_version}

    VersionSpan = struct.Struct({span_fmt!r})

    def iter_spans():
        yield from VersionSpan.iter_unpack(VERSION_SPANS)

    VERSION_SPANS = zlib.decompress(binascii.a2b_base64(
    {b64rows}
    ))
    """).format(ucd_version=ucd_version, span_fmt=span_fmt, b64rows=b64rows)


    outfile.write_text(py_src)
    print(f"Wrote to {outfile}")


def _merge_spans(spans: typing.Iterator[Span]) -> typing.Generator[Span]:
    last = next(spans) 
    merged = 0
    for span in spans:
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

    _write_spans(
        spans,
        ucd_version=ucd_version,
        outfile=PYTHON_OUTFILE,
    )


if __name__ == "__main__":
    main()
