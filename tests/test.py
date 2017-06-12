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

    def test_top_series(self):
        movies = self.service.top_tv_series()
        self.assertNotEqual(0, len(movies))
        self.assertNotEqual(len(movies[0]['title']), None)
        movies = self.service.top_tv_series(top=20)
        self.assertEqual(len(movies), 20)
        movies = self.service.top_tv_series(top=80)
        self.assertEqual(len(movies), 30)
        movies = self.service.top_tv_series(from_year='2010', to_year='2011')
        self.assertNotEqual(0, len(movies))
        self.assertNotEqual(len(movies[0]['title']), None)

    def test_top_premieres(self):
        movies = self.service.top_premieres()
        self.assertNotEqual(0, len(movies))
        self.assertNotEqual(len(movies[0]['title']), None)

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

    def test_top_netflix(self):
        movies = self.service.top_netflix(top=10)
        self.assertEqual(len(movies), 10)
        self.assertNotEqual(len(movies[0]['title']), None)
        self.assertNotEqual(len(movies[0]['rating']), None)

    def test_top_hbo(self):
        movies = self.service.top_hbo(top=10)
        self.assertEqual(len(movies), 10)
        self.assertNotEqual(len(movies[0]['title']), None)

    def test_top_filmin(self):
        movies = self.service.top_filmin(top=10)
        self.assertEqual(len(movies), 10)
        self.assertNotEqual(len(movies[0]['title']), None)
        self.assertNotEqual(len(movies[0]['rating']), None)

    def test_recommend_netflix(self):
        movie = self.service.recommend_netflix()
        self.assertNotEqual(len(movie['title']), None)

    def test_recommend_hbo(self):
        movie = self.service.recommend_hbo()
        self.assertNotEqual(len(movie['title']), None)

    def test_recommend_filmin(self):
        movie = self.service.recommend_filmin()
        self.assertNotEqual(len(movie['title']), None)

    def test_trailer(self):
        movie = self.service.recommend_netflix(trailer=True)
        self.assertNotEqual(len(movie['trailer']), None)

    def test_top_dvd(self):
        movies = self.service.top_dvd(top=10)
        self.assertEqual(len(movies), 10)
        self.assertNotEqual(len(movies[0]['title']), None)
        movies = self.service.top_dvd(top=20)
        self.assertEqual(len(movies), 20)
        movies = self.service.top_dvd(top=80)
        self.assertEqual(len(movies), 40)
        self.assertNotEqual(len(movies[0]['rating']), None)
