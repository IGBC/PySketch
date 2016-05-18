from distutils.core import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='pysketch',
    version='0.1',
    packages=['pysketch'],
    url='https://github.com/IGBC/PySketch',
    license='GPL V3.0',
    author='SEGFAULT',
    author_email='segfault@cbase.org',
    description='python library for Arduino style sketches',
    long_description=read_md("../README.md"),
)
