import argparse
import string
import unicodedata

from . import version
from .unicode_age_db import iter_spans

def parse_codepoint(s):
    s = s.lower()
    if s.startswith("u+"):
        codepoint = int(s.removeprefix("u+"), 16)
    elif s and s[0] in string.digits:
        codepoint = int(s)
    else:
        codepoint = ord(unicodedata.lookup(s))
    return codepoint

def main():
    parser = argparse.ArgumentParser(
            description="Print the version of the Unicode standard where a code point was added")
    parser.add_argument("--debug", metavar="debug", action=argparse.BooleanOptionalAction, help="Show information for debugging the version table")
    parser.add_argument("codepoints", metavar="codepoints", nargs="*", type=str,
                        help="Codepoints to act on")
    args = parser.parse_args()

    if args.debug:
        for i, pi in zip(range(10), iter_spans()):
            print(i, pi)
        return

    if not args.codepoints:
        parser.parse_args(["--help"])
        return

    for cp in args.codepoints:
        i = parse_codepoint(cp)
        try:
            major, minor = version(i)
            vstr = f"{major}.{minor}"
        except ValueError:
            vstr="None"
        uplus = f"U+{i:x}"
        try:
            name = f"\"\\N{{{unicodedata.name(chr(i)).lower()}}}\""
        except ValueError:
            if i < 256:
                name = f"\"\\x{i:02x}\""
            elif i < 65536:
                name = f"\"\\u{i:04x}\""
            else:
                name = f"\"\\U{i:06x}\""
        print(f"{uplus:<8} {name:<60} {vstr:>5}")

if __name__ == '__main__':
    main()
