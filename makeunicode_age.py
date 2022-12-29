from pathlib import Path
import pprint
import re
import string
import sys
from textwrap import dedent


HERE = Path(__file__).parent.resolve()
DERIVEDAGES = HERE.joinpath("DerivedAge.txt")

CYTHON_INFILE = HERE.joinpath("unicode_age.pyx.in")
CYTHON_TEMPLATE = string.Template(CYTHON_INFILE.read_text())


def _write_spans(spans: list, c_out: Path, cython_out: Path):
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

    pyx_src = CYTHON_TEMPLATE.substitute({"numSpans": len(spans)})


    c_out.write_text(c_src)
    print(f"Wrote to {c_out}")

    cython_out.write_text(pyx_src)
    print(f"Wrote to {cython_out}")


def _derivedage_spans():
    CODEPT = r"[0-9A-Fa-f]+"
    PATT = rf"^({CODEPT})(?:\.\.({CODEPT}))?\s*;\s*([\d.]+)\s*#.*"

    with open(DERIVEDAGES, "r") as f:
        for line in f:
            if line.strip() and line.startswith("#"):
                continue
            if m := re.match(PATT, line):
                start, stop, ver = m.groups()
                start = int(start, base=16)
                if stop:
                    stop = int(stop, base=16) + 1
                    stop = min(stop, sys.maxunicode)
                else:
                    stop = start

                major, minor = [int(part) for part in ver.split('.')]

                yield start, stop, major, minor



def main():
    spans = list(_derivedage_spans())

    C_OUTFILE = HERE.joinpath("src", "unicode_age.h")
    CYTHON_OUTFILE = HERE.joinpath("src", "unicode_age.pyx")

    _write_spans(spans, c_out=C_OUTFILE, cython_out=CYTHON_OUTFILE)


if __name__ == "__main__":
    main()
