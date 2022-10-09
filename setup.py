from setuptools import setup
from Cython.Build import cythonize


setup(
    name="unicode_age",
    version="15.0.0",
    ext_modules = cythonize("src/unicode_age.pyx")
)
