"""Client."""
# -*- coding: utf-8 -*-

import requests
import random
from functools import partial
from bs4 import BeautifulSoup

from .config import cache, FIELDS_MOVIE
from .pages import DetailPage, SearchPage, TopPage, TopServicePage, ImagesPage
from .exceptions import FilmAffinityInvalidLanguage

from cachetools import __version__ as cachetools_version
if int(cachetools_version.split('.')[0]) >= 2:
    from cachetools import cached
    from cachetools.keys import hashkey
else:
    from cachetools import cached, hashkey

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


supported_languages = ['en', 'es', 'mx', 'ar', 'cl', 'co']


class Client:
    """Client to make requests to FilmAffinity."""

    base_url = 'https://www.filmaffinity.com/'

    def __init__(self, lang='es'):
        """Init the search service.

        Args:
            lang (str, optional): Language of the page
        """
        if lang not in supported_languages:
            raise FilmAffinityInvalidLanguage(
                lang, supported_languages)
        self.lang = lang
        self.url = self.base_url + self.lang + '/'
        self.url_film = self.url + 'film'
        self.url_images = self.url + 'filmimages.php?movie_id='
        self.url_youtube = 'https://www.youtube.com/results?search_query='

    def _get_trailer(self, title):
        title += ' trailer'
        title = quote(title)
        page = requests.get(self.url_youtube + str(title))
        soup = BeautifulSoup(page.content, "html.parser")
        vid = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]
        return 'https://www.youtube.com' + vid['href']

    def _get_movie_images(self, fa_id):
        url = self.url_images + str(fa_id)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        exist = soup.findAll("div", {"id": 'main-image-wrapper'})
        if not exist:
            return {
                'posters': [],
                'stills': [],
                'promo': [],
                'events': [],
                'shootings': []}
        page = ImagesPage(soup)
        return {
            'posters': page.get_posters(),
            'stills': page.get_stills(),
            'promo': page.get_promos(),
            'events': page.get_events(),
            'shootings': page.get_shootings(),
        }

    def _get_movie_data(self, page, fa_id=None):
        return {
            'id': fa_id or page.get_id(),
            'title': page.get_title(),
            'year': page.get_year(),
            'duration': page.get_duration(),
            'rating': page.get_rating(),
            'votes': page.get_number_of_votes(),
            'description': page.get_description(),
            'directors': page.get_directors(),
            'actors': page.get_actors(),
            'poster': page.get_poster(),
            'country': page.get_country(),
            'genre': page.get_genre(),
            'awards': page.get_awards(),
            'reviews': page.get_reviews(),
        }

    @cached(cache, key=partial(hashkey, id))
    def _get_movie_by_id(self, id, trailer=False, images=False):
        movie = {}
        page = requests.get(self.url_film + str(id) + '.html')
        soup = BeautifulSoup(page.content, "html.parser")
        exist = soup.find_all("div", {"class": 'z-movie'})
        if exist:
            page = DetailPage(soup)
            movie = self._get_movie_data(page, fa_id=id)
            if trailer:
                movie.update({'trailer': self._get_trailer(movie['title'])})
        if images and movie.get('id', False):
            movie.update({'images': self._get_movie_images(movie['id'])})
        return movie

    def _get_movie_by_args(self, key, value, trailer=False, images=False):
        movie = {}
        if key in FIELDS_MOVIE:
            options = '&stype[]=%s' % key
            url = self.url + 'advsearch.php?stext=' + \
                str(value) + options
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            movies_cell = soup.find_all("div", {"class": 'movie-card-1'})
            if movies_cell:
                cell = movies_cell[0]
                id = str(cell['data-movie-id'])
                movie = self._get_movie_by_id(id, 'search', images)
        return movie

    def _return_list_movies(self, page, method, top=10):
        movies = []
        soup = BeautifulSoup(page.content, "html.parser")
        if method == 'top':
            movies_list = soup.find("ul", {"id": 'top-movies'})
            movies_cell = movies_list.find_all(
                "li", {"class": None, "id": None}
            )
            class_ = TopPage
        if method == 'search':
            movies_cell = soup.find_all("div", {"class": 'movie-card'})
            class_ = SearchPage
        if method == 'top_service':
            movies_cell = soup.find_all("div", {"class": 'top-movie'})
            class_ = TopServicePage
        for cell in movies_cell[:top]:
            page = class_(cell)
            movie = self._get_movie_data(page)
            movies.append(movie)
        return movies

    def _recommend(self, service, trailer=False, images=False):
        movie = {}
        url = self.url + 'topcat.php?id=' + service
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        movies_cell = soup.find_all("div", {"class": 'movie-card'})
        cell = random.choice(movies_cell)
        id = str(cell['data-movie-id'])
        movie = self._get_movie_by_id(id, trailer, images)
        return movie

    def _top_service(self, top, service):
        movies = []
        top = 40 if top > 40 else top
        url = self.url + 'topcat.php?id=' + service
        page = requests.get(url)
        movies = self._return_list_movies(page, 'top_service', top)
        return movies
