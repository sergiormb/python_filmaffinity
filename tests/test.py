from unittest import TestCase

import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')

import python_filmaffinity


class TestApi(TestCase):
    service = python_filmaffinity.Filmaffinity()

    def test_search(self):
        movies = self.service.search(title='Batman')
        self.assertNotEqual(0, len(movies))

    def test_get_movie(self):
        movie = self.service.get_movie(id='197671')
        self.assertEqual(
            movie['title'], 'Piratas del Caribe: La venganza de Salazar')

    def test_top_filmaffinity(self):
        movies = self.service.top_filmaffinity()
        self.assertNotEqual(0, len(movies))

    def test_top_premieres(self):
        movies = self.service.top_premieres()
        self.assertNotEqual(0, len(movies))

    def test_top_filmaffinity_years(self):
        movies = self.service.top_filmaffinity(from_year='2010', to_year='2011')
        self.assertNotEqual(0, len(movies))

    def test_search_years(self):
        movies = self.service.search(title='Batman', from_year='2000', to_year='2011')
        self.assertNotEqual(0, len(movies))

    def test_get_movie_title(self):
        movie = self.service.get_movie(title='Celda 211')
        self.assertEqual(
            movie['title'], 'Celda 211')

    def test_get_movie_title_future(self):
        movie = self.service.get_movie(title='Batman')
        self.assertEqual(movie['rating'], None)
