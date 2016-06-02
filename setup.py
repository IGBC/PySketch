import os
from distutils.core import setup


def read_desc(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='sketches',
    version='0.1.0.1',
    packages=['sketches'],
    scripts=['bin/pysketch'],
    url='https://github.com/IGBC/PySketch',
    # license='GPL V3.0',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Console',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Software Development :: Interpreters',
                 'Topic :: Education', ],
    author='IGBC',
    author_email='segfault@c-base.org',
    description='Write Arduino style sketches in Python',
    long_description=read_desc("README.rst"),
)
