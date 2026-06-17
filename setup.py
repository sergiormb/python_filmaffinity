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
    python_requires='>=3.9',
    extras_require={
        'models': [
            'pydantic>=1.10',
        ],
        'dev': [
            'build>=1.0',
            'pydantic>=1.10',
            'pytest>=8.0',
            'twine>=5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'filmaffinity=python_filmaffinity.cli:main',
        ],
    },
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14'
    ]
)
