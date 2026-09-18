from __future__ import annotations

import bisect
import functools
from typing import Tuple

from .unicode_age_db import iter_spans, UCD_VERSION

UCD_VERSION_STR = ".".join(str(it) for it in UCD_VERSION)

UCDVersion = Tuple[int, int]

@functools.cache
def _spans():
    return list(iter_spans())



def version(codept: int) -> UCDVersion | None:
    spans = _spans()
    idx = bisect.bisect_right(spans, (codept+1, codept))
    if idx != 0:
        start, stop, major, minor = spans[idx-1]
        if start <= codept <= stop:
            return (major, minor)

    # search failed
    raise ValueError(f"Codepoint U+{codept:x} was not allocated as of UCD {UCD_VERSION_STR}")
