from unittest import TestCase
import time
import sys
import os
import random

import python_filmaffinity
from python_filmaffinity.config import FIELDS_PAGE_MOVIES, FIELDS_PAGE_DETAIL
from python_filmaffinity.exceptions import (
    FilmAffinityInvalidLanguage,
    FilmAffinityInvalidBackend,
    FilmAffinityConnectionError
)
import python_filmaffinity.__meta__ as meta_test

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')


class TestApi(TestCase):
    service = python_filmaffinity.FilmAffinity()

    def check_list(self, movies):
        self.assertNotEqual(0, len(movies))
        movie = random.choice(movies)
        for field in FIELDS_PAGE_MOVIES:
            self.assertNotEqual(
                movie[field], None,
                msg='Error on getting movie list '
                    ',field is: {}'.format(field))
        self.assertNotEqual(len(movie['directors']), 0)

    def check_element(self, movie):
        for field in FIELDS_PAGE_DETAIL:
            self.assertNotEqual(
                movie[field], None,
                msg='Error on checking movie '
                    'field: {}'.format(field))

    def test_search(self):
        movies = self.service.search(title='Batman')
        self.check_list(movies)

    def test_get_movie(self):
        movie = self.service.get_movie(id='197671', images=True)
        self.check_element(movie)
        self.assertNotEqual(
            movie['images'], [],
            msg='Error on getting movie images')

    def test_top_filmaffinity(self):
        time.sleep(3)
        movies = self.service.top_filmaffinity()
        self.check_list(movies)

    def test_top_series(self):
        # For renovate the headers 
        self.service = python_filmaffinity.FilmAffinity()
        movies = self.service.top_tv_series()
        self.check_list(movies)
        movies = self.service.top_tv_series(top=5)
        self.assertEqual(len(movies), 5)
        movies = self.service.top_tv_series(top=80)
        self.assertEqual(len(movies), 30)
        movies = self.service.top_tv_series(from_year='2010', to_year='2011')
        self.check_list(movies)

    def test_top_premieres(self):
        time.sleep(3)
        movies = self.service.top_premieres()
        self.check_list(movies)

    def test_top_filmaffinity_years(self):
        time.sleep(3)
        movies = self.service.top_filmaffinity(
            from_year='2010', to_year='2011')
        self.check_list(movies)

    def test_search_years(self):
        time.sleep(3)
        movies = self.service.search(
            title='Batman', from_year='2000', to_year='2011')
        self.check_list(movies)

    def test_top_netflix(self):
        time.sleep(3)
        movies = self.service.top_netflix(top=10)
        self.check_list(movies)

    def test_top_movistar(self):
        # For renovate the headers 
        self.service = python_filmaffinity.FilmAffinity()
        movies = self.service.top_movistar(top=10)
        self.check_list(movies)

    def test_top_rakuten(self):
        movies = self.service.top_rakuten(top=10)
        self.check_list(movies)

    def test_top_hbo(self):
        time.sleep(3)
        movies = self.service.top_hbo(top=10)
        self.check_list(movies)

    def test_top_filmin(self):
        movies = self.service.top_filmin(top=10)
        self.check_list(movies)

    def test_recommend_netflix(self):
        time.sleep(3)
        movie = self.service.recommend_netflix()
        self.check_element(movie)

    def test_recommend_hbo(self):
        movie = self.service.recommend_hbo()
        self.check_element(movie)

    def test_recommend_filmin(self):
        time.sleep(3)
        movie = self.service.recommend_filmin()
        self.check_element(movie)

    def test_recommend_movistar(self):
        time.sleep(3)
        movie = self.service.recommend_movistar()
        self.check_element(movie)

    def test_recommend_rakuten(self):
        # For renovate the headers 
        self.service = python_filmaffinity.FilmAffinity()
        movie = self.service.recommend_rakuten()
        self.check_element(movie)

    def test_top_dvd(self):
        time.sleep(3)
        # For renovate the headers 
        self.service = python_filmaffinity.FilmAffinity()
        movies = self.service.top_dvd(top=10)
        self.check_list(movies)
        movies = self.service.top_dvd(top=20)
        self.assertEqual(len(movies), 20)
        movies = self.service.top_dvd(top=80)
        self.assertEqual(len(movies), 40)
        self.check_list(movies)

    def test_invalid_language(self):
        self.assertRaises(
            FilmAffinityInvalidLanguage,
            python_filmaffinity.FilmAffinity, lang="abc")

    def test_invalid_backend(self):
        self.assertRaises(
            FilmAffinityInvalidBackend,
            python_filmaffinity.FilmAffinity, cache_backend='mysqlite')

    def test_invalid_connection(self):
        self.assertRaises(
            FilmAffinityConnectionError,
            self.service._load_url, "http://notworking.tz",
            headers={'User-Agent': 'Mozilla/5.0'}, verify=True,
            timeout=1, force_server_response=True)

    def test_meta_variables(self):
        for v in meta_test.__dict__:
            if v in ['__builtins__', '__package__', '__doc__']:
                continue
            self.assertIsNotNone(
                meta_test.__dict__[v],
                msg='Error on getting meta value: {}'.format(v))
