"""
omdb
====

Python wrapper for OMDbAPI.com.

Project: https://github.com/dgilland/omdb.py
"""

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open("README.rst", "r") as fh:
    long_description = fh.read()

meta = {}
exec(read('python_filmaffinity/__meta__.py'), meta)

setup(
    name=meta['__title__'],
    version=meta['__version__'],
    url=meta['__url__'],
    setup_requires=[],
    license=meta['__license__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description=meta['__summary__'],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # this must be the same as the name above
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                    "tests", "*tests*"]),
    install_requires=meta['__install_requires__'],
    zip_safe=False,
    # use the URL to the github repo
    download_url='https://github.com/sergiormb/python_filmaffinity/tarball/' \
    + meta['__version__'],
    keywords='filmaffinity movies films',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)
