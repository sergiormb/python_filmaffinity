# -*- coding: utf-8 -*-
from .__meta__ import  *
from .client import Client
from .config import FIELDS_TYPE


class FilmAffinity(Client):

    def get_movie(self, trailer=False, images=False, **kwargs):
        """Return a dictionary with the data of the movie.

        Args:
            title: Search by title
            id: Search by id
            trailer: Enable/Disable search a trailer
            images: Enable/Disable search for images
        Returns:
            TYPE: Dictionary with movie data
        """
        movie = {}
        if kwargs is not None:
            for key, value in iter(kwargs.items()):
                if key == 'id':
                    movie = self._get_movie_by_id(
                        value, trailer, images)
                else:
                    movie = self._get_movie_by_args(
                        key, value, trailer, images)
        return movie

    def search(self, top=10, **kwargs):
        """Return a list with the data of the movies.

        Args:
            title: Search by title
            director: Search by director
            cast: Search by cast
            from_year: Search from the year
            to_year: Search until the year
            genre: 
                AN: Animación
                AV: Aventuras
                BE: Bélico
                C-F: Ciencia Ficción
                F-N: Cine Negro
                CO: Comedia
                DESC: Desconocido
                DO: Documental
                DR: Drama
                FAN: Fantástico
                INF: Infantil
                INT: Intriga
                MU: Musical
                RO: Romance
                TV_SE: Serie de TV
                TE: Terror
                WE: Western
        Returns:
            TYPE: Lis with movies data
        """
        top = 20 if top > 20 else top
        movies = []
        if kwargs is not None:
            options = ''
            simple_search = 'title' in kwargs
            for key, value in iter(kwargs.items()):
                if key in FIELDS_TYPE:
                    if (key != 'title'):
                        simple_search = False
                    options += 'stext=%s&stype[]=%s&' % (str(kwargs[key]), key)
                if key == 'from_year':
                    options += 'fromyear=%s&' % value
                if key == 'to_year':
                    options += 'toyear=%s&' % value
                if key == 'genre':
                    options += 'genre=%s&' % value
            if (simple_search):
                options = 'stype=title&stext=' + str(kwargs['title'])
                url = self.url + 'search.php?' + options
            else:
                url = self.url + 'advsearch.php?' + options
            page = self._load_url(url)
            movies = self._return_list_movies(page, 'search', top)
            if (len(movies) == 0):
                url = self.url + 'advsearch.php?' + options
                page = self._load_url(url)
                movies = self._return_list_movies(page, 'search', top)
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
        page = self._load_url(url)
        movies = self._return_list_movies(page, 'top', top)
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
        page = self._load_url(url)
        movies = self._return_list_movies(page, 'top', top)
        return movies

    def top_dvd(self, top=10):
        """Return a list with the top new dvds.

        Returns:
            TYPE: Lis with movies data
        """
        top = 40 if top > 40 else top
        movies = []
        if self.lang == 'es':
            url = self.url + 'topcat_new_sa_es.html'
        else:
            url = self.url + 'topcat_DVD_VID_US.html'
        page = self._load_url(url)
        movies = self._return_list_movies(page, 'top_service', top)
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
        page = self._load_url(url)
        movies = self._return_list_movies(page, 'top_service', top)
        return movies

    def top_netflix(self, top=10):
        """Return a list with the top netflix movies.

        Returns:
            TYPE: Lis with movies data
        """
        return self._top_service(top, 'new_netflix')

    def top_hbo(self, top=10):
        """Return a list with the top hbo movies.

        Returns:
            TYPE: Lis with movies data
        """
        return self._top_service(top, 'new_hbo_es')

    def top_filmin(self, top=10):
        """Return a list with the top filmin movies.

        Returns:
            TYPE: Lis with movies data
        """
        return self._top_service(top, 'new_filmin')

    def top_movistar(self, top=10):
        """Return a list with the top movistar movies.

        Returns:
            TYPE: Lis with movies data
        """
        return self._top_service(top, 'new_movistar_f')

    def top_rakuten(self, top=10):
        """Return a list with the top rakuten movies.

        Returns:
            TYPE: Lis with movies data
        """
        return self._top_service(top, 'new_rakuten')

    def recommend_netflix(self, trailer=False, images=False):
        """Return a movie random in Netflix.

        Returns:
            TYPE: Movie data
        """
        return self._recommend('new_netflix', trailer, images)

    def recommend_hbo(self, trailer=False, images=False):
        """Return a movie random in HBO.

        Returns:
            TYPE: Movie data
        """
        return self._recommend('new_hbo_es', trailer, images)

    def recommend_movistar(self, trailer=False, images=False):
        """Return a movie random in Movistar.

        Returns:
            TYPE: Movie data
        """
        return self._recommend('new_movistar_f', trailer, images)

    def recommend_rakuten(self, trailer=False, images=False):
        """Return a movie random in Rakuten.

        Returns:
            TYPE: Movie data
        """
        return self._recommend('new_rakuten', trailer, images)

    def recommend_filmin(self, trailer=False, images=False):
        """Return a movie random in Filmin.

        Returns:
            TYPE: Movie data
        """
        return self._recommend('new_filmin', trailer, images)
