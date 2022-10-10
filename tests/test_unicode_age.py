import unicode_age

import pytest


def test_version():
    assert unicode_age.version(ord("\N{SNAKE}")) == (6, 0)


def test_version_endofspan():
    # Regression test: at one point, the ends of version spans given in DerivedAge.txt weren't being handled correctly
    assert unicode_age.version(0x0903) == (1, 1)


def test_version_badtype():
    with pytest.raises(TypeError):
        unicode_age.version("\N{SNAKE}")
