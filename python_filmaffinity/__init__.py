# -*- coding: utf-8 -*-
import requests
from .client import Client
from .config import FIELDS_TYPE


class Filmaffinity(Client):

    base_url = 'https://www.filmaffinity.com/'

    def __init__(self, lang='es'):
        """Init the search service.

        Args:
            lang (str, optional): Language of the page
        """
        self.lang = lang
        self.url = self.base_url + self.lang + '/'
        self.url_film = self.url + 'film'
        self.url_youtube = 'https://www.youtube.com/results?search_query='

    def get_movie(self, trailer=False, **kwargs):
        """Return a dictionary with the data of the movie.

        Args:
            title: Search by title
            id: Search by id
        Returns:
            TYPE: Dictionary with movie data
        """
        movie = {}
        if kwargs is not None:
            for key, value in iter(kwargs.items()):
                if key == 'id':
                    movie = self._get_movie_by_id(value, trailer)
                else:
                    movie = self._get_movie_by_args(key, value, trailer)
        return movie

    def search(self, **kwargs):
        """Return a list with the data of the movies.

        Args:
            title: Search by title
            director: Search by director
            cast: Search by cast
            from_year: Search from the year
            to_year: Search until the year
        Returns:
            TYPE: Lis with movies data
        """
        movies = []
        if kwargs is not None:
            options = ''
            for key, value in iter(kwargs.items()):
                if key in FIELDS_TYPE:
                    options += 'stext=%s&stype[]=%s&' % (str(kwargs[key]), key)
                if key == 'from_year':
                    options += 'fromyear=%s&' % value
                if key == 'to_year':
                    options += 'toyear=%s&' % value
            url = self.url + 'advsearch.php?' + options
            page = requests.get(url)
            movies = self._return_list_movies(page=page, from_search=True)
        return movies

    def top_filmaffinity(self, top=10, **kwargs):
        """Return a list with the top filmaffinity movies.

        Args:

            from_year: Search from the year
            to_year: Search until the year
        Returns:
            TYPE: Lis with movies data
        """
        top = 30 if top > 30 else top
        movies = []
        if kwargs is not None:
            options = ''
            for key, value in iter(kwargs.items()):
                if key == 'from_year':
                    options += 'fromyear=%s&' % value
                if key == 'to_year':
                    options += 'toyear=%s&' % value
        if options:
            url = self.url + 'topgen.php?' + options
        else:
            url = self.url + 'topgen.php'
        page = requests.get(url)
        movies = self._return_list_movies(page, top, True)
        return movies

    def top_tv_series(self, top=10, **kwargs):
        """Return a list with the top tv series.

        Args:

            from_year: Search from the year
            to_year: Search until the year
        Returns:
            TYPE: Lis with movies data
        """
        top = 30 if top > 30 else top
        movies = []
        if kwargs is not None:
            options = ''
            for key, value in iter(kwargs.items()):
                if key == 'from_year':
                    options += 'fromyear=%s&' % value
                if key == 'to_year':
                    options += 'toyear=%s&' % value
        if options:
            url = self.url + 'topgen.php?genre=TV_SE&' + options
        else:
            url = self.url + 'topgen.php?genre=TV_SE'
        page = requests.get(url)
        movies = self._return_list_movies(page, top, True)
        return movies

    def top_dvd(self, top=10):
        """Return a list with the top new dvds.

        Returns:
            TYPE: Lis with movies data
        """
        top = 40 if top > 40 else top
        movies = []
        if self.lang == 'es':
            url = 'topcat_new_sa_es.html'
        else:
            url = 'topcat_DVD_VID_US.html'
        page = requests.get(url)
        movies = self._return_list_movies(page, top)
        return movies

    def top_premieres(self, top=10):
        """Return a list with the top filmaffinity movies.

        Args:

            from_year: Search from the year
            to_year: Search until the year
        Returns:
            TYPE: Lis with movies data
        """
        top = 40 if top > 40 else top
        movies = []
        url = self.url + 'topcat_new_th_es.html'
        page = requests.get(url)
        movies = self._return_list_movies(page, top)
        return movies

    def top_netflix(self, top=10):
        """Return a list with the top netflix movies.

        Returns:
            TYPE: Lis with movies data
        """
        movies = self._top_service(top, 'new_netflix')
        return movies

    def top_hbo(self, top=10):
        """Return a list with the top hbo movies.

        Returns:
            TYPE: Lis with movies data
        """
        movies = self._top_service(top, 'new_hbo_es')
        return movies

    def top_filmin(self, top=10):
        """Return a list with the top filmin movies.

        Returns:
            TYPE: Lis with movies data
        """
        movies = self._top_service(top, 'new_filmin')
        return movies

    def recommend_netflix(self, trailer=False):
        """Return a movie random in Netflix.

        Returns:
            TYPE: Movie data
        """
        movies = self._recommend('new_netflix', trailer)
        return movies

    def recommend_hbo(self, trailer=False):
        """Return a movie random in HBO.

        Returns:
            TYPE: Movie data
        """
        movies = self._recommend('new_hbo_es', trailer)
        return movies

    def recommend_filmin(self, trailer=False):
        """Return a movie random in Filmin.

        Returns:
            TYPE: Movie data
        """
        movies = self._recommend('new_filmin', trailer)
        return movies
