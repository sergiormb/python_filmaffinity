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
