# `unicode_age`

A small extension module for determining what version a Unicode codepoint was
added to the standard

## Example usage

```python
>>> import unicode_age
>>> codept = ord("\N{SNAKE}")
>>> print(unicode_age.version(codept))
(6, 0)
```

## Updating

The script `makeunicode_age.py` consumes
[`DerivedAge.txt`](https://www.unicode.org/reports/tr44/#DerivedAge.txt) and
produces the header file that holds the backing data for this module and fills
in the number of spans in the Cython template. To make a build for another
version of the Unicode Character Database, you should be able to replace
`DerivedAge.txt` and re-run this script.
