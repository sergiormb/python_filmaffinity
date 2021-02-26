*******************
Python FilmAffinity
*******************
This is a simple python scraping for the FilmAffinity.

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

Pip
***
::

    pip install python-filmaffinity


From Source
***********

::

    git clone git@github.com:sergiormb/python_filmaffinity.git
    cd python_filmaffinity
    python setup.py install


Requirements
**********************

::

    requests >= 2.0.1
    requests-cache >= 0.4.13
    bs4 >= 0.0.1


Examples
========

.. code-block:: python

    import python_filmaffinity
    service = python_filmaffinity.FilmAffinity()
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

language
********

- Spanish: 'es'
- USA, UK: 'en'
- México: 'mx'
- Argentina: 'ar'
- Chile: 'cl'
- Colombia: 'co'


- Example

.. code-block:: python

    import python_filmaffinity
    service = python_filmaffinity.FilmAffinity(lang='en')


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
| id        |   False  | String | FilmAffinity id                   |
+-----------+----------+--------+-----------------------------------+
| title     |   False  | String | Get movie by title                |
+-----------+----------+--------+-----------------------------------+
| trailer   |   False  | Boolean| Return movie with trailer         |
+-----------+----------+--------+-----------------------------------+
| images    |   False  | Boolean| Return movie with images          |
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
| top       |   False  | Integer| Number of elements                |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.top_filmaffinity()
    movies = service.top_filmaffinity(from_year=2010, to_year=2011)


top_premieres
*************

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| top       |   False  | Integer| Number of elements                |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.top_premieres()


top_netflix, top_hbo, top_filmin, top_movistar, top_rakuten, top_tv_series
**************************************************************************

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| top       |   False  | Integer| Number of elements                |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.top_netflix()
    movies = service.top_hbo(top=5)
    movies = service.top_filmin()
    movies = service.top_movistar()
    movies = service.top_rakuten()
    movies = service.top_tv_series()


recommend HBO, Netflix, Filmin, Movistar, Rakuten
*************************************************

+-----------+----------+--------+-----------------------------------+
| Parameter | Required |   Type | Description                       |
+===========+==========+========+===================================+
| trailer   |   False  | Boolean| Return movie with trailer         |
+-----------+----------+--------+-----------------------------------+
| images    |   False  | Boolean| Return movie with images          |
+-----------+----------+--------+-----------------------------------+

- Example

.. code-block:: python

    movies = service.recommend_netflix()
    movies = service.recommend_hbo()
    movies = service.recommend_filmin()
    movies = service.recommend_movistar()
    movies = service.recommend_rakuten()


Changelog
=========

v0.0.18 (26-02-2021)
********************

- When images are requested, lets provide also the country where
  they were published (@jcea)
- Correctly provide the trailers listed in filmaffinity (@jcea)
- Spurious search in youtube deleted (@jcea)
- Extract correctly when multiple genres (@jcea)
- Added "writers", "music", "cinematography" and "producers" (@jcea)
- Regression processing "original_title" in searches (@jcea)

v0.0.17 (18-02-2021)
********************

- Deleted spaces at the end of the title (@jcea)
- Added original_title (@jcea)
- Fix directors scraping (@jcea)

v0.0.15 (03-08-2020)
********************

- Search by genre

v0.0.14 (08-09-2018)
********************

- Fixed errors

v0.0.13 (07-09-2018)
********************

- Adds proxies and random user-agent in headers

v0.0.12 (27-08-2018)
********************

- Changed description

v0.0.11 (27-08-2018)
********************

- Fixed errors

v0.0.1O (27-08-2018)
********************

- Fixed errors with SSL

v0.0.09 (28-12-2017)
********************

- Replaces cachetools for requests-cache

v0.0.8 (26-12-2017)
*******************

- Add images
- Fixed errors

v0.0.7 (15-12-2017)
*******************

- Fixes encoding for the analyzed results
- Disabled limitations for all the supported languages
- Change of name to the main class.
- Adds initial language check and raise error if this is not in support
- Adds basic exceptions

v0.0.6 (12-06-2017)
*******************

- Add cachetools

v0.0.5 (13-06-2017)
*******************

- Fixed errors

v0.0.4 (11-06-2017)
*******************

- Top new DVDs
- Get movie with trailer
- Top TV series
- Return movies list with raiting


v0.0.3 (10-06-2017)
*******************

- Top Netlfix, HBO and Filmin
- Recommendation from Netflix, HBO or Filmin
- Fixed errors


v0.0.2 (31-05-2017)
*******************

- Search movies by title, year, director or cast.
- Get the filmaffinity top and search by year
- Get the premieres top


v0.0.1 (29-05-2017)
*******************

- Initial release.


Authors
*******


Lead
====

- Sergio Pino, sergiormb88@gmail.com, `sergiormb.github.io <https://sergiormb.github.io>`_

Collaborators
=============

- opacam https://github.com/opacam
- jcea - https://www.jcea.es/ - https://blog.jcea.es/ - https://github.com/jcea

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
