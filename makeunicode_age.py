from __future__ import annotations
import inspect
import pprint
import re
import string
import struct
import sys
from pathlib import Path
from textwrap import dedent


HERE = Path(__file__).parent.resolve()
DERIVEDAGES = HERE.joinpath("DerivedAge.txt")

CYTHON_INFILE = HERE.joinpath("unicode_age.pyx.in")
CYTHON_TEMPLATE = string.Template(CYTHON_INFILE.read_text())


def _write_spans_c(spans: list, outfile: Path):
    c_src = dedent("""
    // 8 + 8 + 2 = 18 bytes per span
    // 1283 'real' spans, 435 singleton spans as of Unicode 15.0
    // ~31 KB of storage required (in practice the actual consumed memory is ~21 KB? not sure why that is...)
    typedef struct {
            int start;
            int stop;
            char major;
            char minor;
    } versionSpan_t;


    static const versionSpan_t versionSpans[] = {
    """)

    c_src += "\t"

    for (start, stop, major, minor) in spans:
        line = f"{{0x{start:06x}, 0x{stop:06x}, {major}, {minor}}}"
        c_src += f"{line},\n\t"

    c_src += "\n};"

    outfile.write_text(c_src)


def _write_spans_py(spans: list, ucd_version: tuple[int], outfile: Path):
    span_fmt = "iibb"
    VersionSpan = struct.Struct(span_fmt)

    Nbytes = len(spans) * VersionSpan.size
    buf = bytearray(Nbytes)

    for n, s in enumerate(spans):
        VersionSpan.pack_into(buf, n*VersionSpan.size, *s)

    py_src = dedent(f"""
    from __future__ import annotations
    import struct

    UCD_VERSION = {ucd_version}

    VersionSpan = struct.Struct({span_fmt!r})

    def iter_spans():
        yield from VersionSpan.iter_unpack(VERSION_SPANS)

    VERSION_SPANS = {repr(buf)}
    """)

    outfile.write_text(py_src)


def _write_spans(spans: list, ucd_version: tuple, c_out: Path, cython_out: Path, python_out: Path):
    _write_spans_c(spans, c_out)
    print(f"Wrote to {c_out}")

    pyx_src = CYTHON_TEMPLATE.substitute({"numSpans": len(spans)})
    cython_out.write_text(pyx_src)
    print(f"Wrote to {cython_out}")

    _write_spans_py(spans, ucd_version=ucd_version, outfile=python_out)
    print(f"Wrote to {python_out}")


def _derivedage_spans(fn):
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

                yield start, stop, major, minor


def parse_ucdversion(fn: Path) -> tuple[int, int, int]:
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
    spans = list(_derivedage_spans(DERIVEDAGES))

    UNICODE_AGE = HERE.joinpath("src", "unicode_age")
    C_OUTFILE = HERE.joinpath("src", "unicode_age.h")
    CYTHON_OUTFILE = HERE.joinpath("src", "unicode_age.pyx")
    PYTHON_OUTFILE = UNICODE_AGE.joinpath("unicode_age_db.py")

    _write_spans(
        spans,
        ucd_version=ucd_version,
        c_out=C_OUTFILE,
        cython_out=CYTHON_OUTFILE,
        python_out=PYTHON_OUTFILE,
    )


if __name__ == "__main__":
    main()
