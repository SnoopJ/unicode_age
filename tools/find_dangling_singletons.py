from pathlib import Path
import re
import sys


HERE = Path(__file__).parent.resolve()
DERIVEDAGES = HERE.joinpath("DerivedAge.txt")

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
    spans = set(_derivedage_spans())

    for (a, b, *truever) in spans:
        if (a == b):  # for singleton spans
            for (start, stop, *ver) in spans:
                if start != stop and stop == b:  # for spans whose boundary abuts the singleton under consideration
                    print(f"({b:06x}, {tuple(truever)}),")


if __name__ == "__main__":
    main()
