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
    movie_models = service.search(title='Batman', as_model=True)


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
    movie_model = service.get_movie(id='495280', as_model=True)


exporters
*********

- Example

.. code-block:: python

    movies = service.search(title='Batman')
    python_filmaffinity.to_json(movies, 'movies.json')
    python_filmaffinity.to_csv(movies, 'movies.csv')
    python_filmaffinity.to_markdown(movies, 'movies.md')


command line
************

- Example

.. code-block:: bash

    filmaffinity search "Batman" --top 5
    filmaffinity movie 197671 --images --json
    filmaffinity top --kind filmaffinity --top 10


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
