from distutils.core import setup
from pypandoc import convert


def read_md(file):
    convert(file, 'rst')

setup(
    name='sketches',
    version='0.1',
    packages=['sketches'],
    url='https://github.com/IGBC/PySketch',
    license='GPL V3.0',
    author='SEGFAULT',
    author_email='segfault@cbase.org',
    description='python library for Arduino style sketches',
    long_description=read_md("../README.md"),
)
