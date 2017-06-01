*******************
Python Filmaffinity
*******************
This is a simple python scraping for the Filmaffinity.

.. image:: https://travis-ci.org/sergiormb/python_filmaffinity.svg?branch=master
    :target: https://travis-ci.org/sergiormb/python_filmaffinity
.. image:: https://coveralls.io/repos/github/sergiormb/python_filmaffinity/badge.svg?branch=master
    :target: https://coveralls.io/github/sergiormb/python_filmaffinity?branch=master
.. image:: https://img.shields.io/github/license/mashape/apistatus.svg   
    :target: https://github.com/sergiormb/python_filmaffinity/blob/master/LICENSE.rst
.. image:: https://img.shields.io/pypi/pyversions/Django.svg   
    :target: https://pypi.python.org/pypi/python_filmaffinity/
.. image:: https://readthedocs.org/projects/python-filmaffinity/badge/?version=latest
    :target: http://python-filmaffinity.readthedocs.io/en/latest/?badge=latest


Installation
============

**omdb** requires Python >= 2.6 or >= 3.4.

To install from `PyPi <https://pypi.python.org/pypi/omdb>`_:

::

    pip install omdb


Pip
***
::

    pip install python_filmaffinity


From Source
***********

::

    git clone git@github.com:sergiormb/python_filmaffinity.git`
    cd python_filmaffinity`
    python setup.py install`


Requirements
**********************

::

    requests >= 2.0.1`
    bs4 >= 0.0.1`


Examples
========

.. code-block:: python

    import python_filmaffinity
    service = python_filmaffinity.Filmaffinity()
    movie = service.get_movie(title='Celda 211')
    movie['title']
    Celda 211
    movie['rating']
    7.7
    movie['directors']
    ['Daniel Monzón']
    movie['actors']
    ['Luis Tosar', 'Alberto Ammann', 'Antonio Resines', 'Carlos Bardem', 'Marta Etura', 'Vicente Romero', 'Manuel Morón', 'Manolo Solo', 'Fernando Soto', 'Luis Zahera', 'Patxi Bisquert', 'Félix Cubero', 'Josean Bengoetxea', 'Juan Carlos Mangas', 'Jesús Carroza']

Usage
=====


search
******

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| title     |   False  | String | Search for the title of the movie |
+-----------+----------+--------+-----------------------------------+
| cast      |   False  | String | Search movies by actor            |
+-----------+----------+--------+-----------------------------------+
| director  |   False  | String | Search movies by the director     |
+-----------+----------+--------+-----------------------------------+
| from_year |   False  | String | Search start date                 |
+-----------+----------+--------+-----------------------------------+
| to_year   |   False  | String | Search end date                   |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.search(cast='Nicolas Cage')


get_movie
*********

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| id        |   False  | String | Filmaffinity id                   |
+-----------+----------+--------+-----------------------------------+
| title     |   False  | String | Get movie by title                |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.get_movie(title='Avatar')
    movies = service.get_movie(id='495280')


top_filmaffinity
****************

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| from_year |   False  | String | Search start date                 |
+-----------+----------+--------+-----------------------------------+
| to_year   |   False  | String | Search end date                   |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.top_filmaffinity()
    movies = service.top_filmaffinity(from_year=2010, to_year=2011)


top_premieres
*************

- Example

.. code-block:: python

    movies = service.top_premieres()

Usage
=====


search
******

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| title     |   False  | String | Search for the title of the movie |
+-----------+----------+--------+-----------------------------------+
| cast      |   False  | String | Search movies by actor            |
+-----------+----------+--------+-----------------------------------+
| director  |   False  | String | Search movies by the director     |
+-----------+----------+--------+-----------------------------------+
| from_year |   False  | String | Search start date                 |
+-----------+----------+--------+-----------------------------------+
| to_year   |   False  | String | Search end date                   |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.search(cast='Nicolas Cage')


get_movie
*********

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| id        |   False  | String | Filmaffinity id                   |
+-----------+----------+--------+-----------------------------------+
| title     |   False  | String | Get movie by title                |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.get_movie(title='Avatar')
    movies = service.get_movie(id='495280')


top_filmaffinity
****************

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| from_year |   False  | String | Search start date                 |
+-----------+----------+--------+-----------------------------------+
| to_year   |   False  | String | Search end date                   |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.top_filmaffinity()
    movies = service.top_filmaffinity(from_year=2010, to_year=2011)


top_premieres
*************

- Example

.. code-block:: python

    movies = service.top_premieres()

Authors
*******


Lead
====

- Sergio Pino, sergiormb88@gmail.com, `sergiormb.github.io <https://sergiormb.github.io>`_

License
=======

The MIT License (MIT)

Copyright (c) 2014 Derrick Gilland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
