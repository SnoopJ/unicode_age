cdef extern from "unicode_age.h":
    struct versionSpan:
        int start
        int stop
        char major
        char minor

    # Cython requires a hardcoded size here
    versionSpan[1718] versionSpans


NUM_SPANS = 1718


cdef _version(codept):
    # A linear scan over known version spans is probably fine? There are "only"
    # ~2000 of them in 15.0

    # NOTE: I want to do `for span in versionSpans` here but the generated C
    # confuses the compiler (error messages about the unknown size of the
    # versionSpan wrapper)
    for n in range(NUM_SPANS):
        if versionSpans[n].start <= codept <= versionSpans[n].stop:
            return versionSpans[n].major, versionSpans[n].minor

    # linear scan failed
    raise ValueError("Not found")


def version(codept):
    return _version(codept)
