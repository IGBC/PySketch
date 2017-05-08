from setuptools import setup, find_packages

from sketches import __version__

setup(
    name='sketches',
    version=__version__,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points = {
        'console_scripts': ['pysketch=sketches:main'],
    },
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
    long_description='Write Arduino style sketches in Python\nSee: https://github.com/IGBC/PySketch',
)
