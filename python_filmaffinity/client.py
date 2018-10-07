#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import requests_cache
import random

from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from inspect import getsourcefile
from os.path import join, dirname, abspath
from .config import FIELDS_MOVIE
from .pages import DetailPage, SearchPage, TopPage, TopServicePage, ImagesPage
from .exceptions import (
    FilmAffinityInvalidLanguage,
    FilmAffinityInvalidBackend,
    FilmAffinityConnectionError)
from .proxies import get_random_proxy
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

current_folder = dirname(abspath(getsourcefile(lambda: 0)))
supported_languages = ['en', 'es', 'mx', 'ar', 'cl', 'co']


class Client:
    """Client to make requests to FilmAffinity.
        Args:
            lang: Language, one of: ('en', 'es', 'mx', 'ar', 'cl', 'co')
            cache_path: Path to FilmAffinity Database (If not set, the
                database will be stored inside python_filmaffinity path)
            cache_backend: One of (sqlite, mongodb, memory, redis). Set to
                memory or None if you don't wont persistent cache
                (defaults to sqlite).
                Note for backends (from requests-cache docs):
                    'sqlite' - sqlite database
                    'memory' - not persistent,
                        stores all data in Python dict in memory
                    'mongodb' - (experimental) MongoDB database
                        (pymongo < 3.0 required)
                    'redis' - stores all data on a redis data store
                        (redis required)
            cache_expires: Time in seconds to force new requests from the
                server (defaults to 86400, 24 hours)
            cache_remove_expired: Force to remove expired responses after any
                requests call. This will ensure that if any call to
                FilmAffinity fails and we already made that call we will get a
                response at a cost of a bigger database file (defaults to True)

    """

    base_url = 'https://www.filmaffinity.com/'

    def __init__(self, lang='es', cache_path=None,
                 cache_backend='sqlite', cache_expires=86400,
                 cache_remove_expired=True):
        """Init the search service.

        Args:
            lang (str, optional): Language of the page
        """
        if lang not in supported_languages:
            raise FilmAffinityInvalidLanguage(
                lang, supported_languages)
        if cache_backend not in ['sqlite', 'memory', 'mongodb', 'redis', None]:
            raise FilmAffinityInvalidBackend(
                cache_backend)
        self.lang = lang

        self.url = self.base_url + self.lang + '/'
        self.url_film = self.url + 'film'
        self.url_images = self.url + 'filmimages.php?movie_id='
        self.url_youtube = 'https://www.youtube.com/results?search_query='

        # initialize requests-cache
        self.cache_expires = cache_expires
        self.cache_backend = cache_backend if cache_backend else 'memory'
        self.cache_path = self._get_cache_file(cache_path)
        self.cache_remove_expired = cache_remove_expired
        self.session = None
        self.session_headers = {
            'User-Agent': generate_user_agent(
                device_type="desktop", os=('mac', 'linux')
            )
        }

    def _generate_new_session_headers(self):
        self.session_headers = {
            'User-Agent': generate_user_agent(
                device_type="desktop", os=('mac', 'linux')
            )
        }

    def _get_cache_file(self, cache_path=None):
        """Returns the cache file used by requests-cache
        """
        c = None
        if self.cache_backend in ['memory']:
            p = 'cache'
        elif cache_path:
            c = join(cache_path, "cache-film-affinity")
        else:
            c = join(current_folder, "cache-film-affinity")
        return c

    def _get_requests_session(self):
        """Initialize requests Session"""
        self.session = requests_cache.CachedSession(
            expire_after=self.cache_expires,
            backend=self.cache_backend,
            cache_name=self.cache_path,
            include_get_headers=True,
            old_data_on_error=True
            )
        if self.cache_remove_expired:
            self.session.remove_expired_responses()

    def _load_url(self, url, headers=None, verify=None,
                  timeout=3, force_server_response=False):
        """Return response from The FilmAffinity"""
        self._generate_new_session_headers()
        kwargs = {'headers': self.session_headers}
        proxies = get_random_proxy()
        if proxies:
            kwargs.update({"proxies": proxies})
        if headers:
            kwargs['verify'] = verify
        if headers:
            kwargs['headers'] = headers
        if timeout:
            kwargs['timeout'] = timeout
        if not self.session:
            self._get_requests_session()
        try:
            if not force_server_response:
                response = self.session.get(url, **kwargs)
            else:
                with self.session.cache_disabled():
                    response = self.session.get(url, **kwargs)
        except requests.exceptions.ConnectionError as er:
            raise FilmAffinityConnectionError(er)
        return response

    def _get_trailer(self, title):
        url_video = None
        title += ' trailer'
        title = title.encode("utf-8")
        title = quote(title)
        page = self._load_url(self.url_youtube + str(title))
        soup = BeautifulSoup(page.content, "html.parser")
        vid = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
        if vid:
            vid = vid[0]
            url_video = 'https://www.youtube.com' + vid['href']
        return url_video

    def _get_movie_images(self, fa_id):
        url = self.url_images + str(fa_id)
        r = self._load_url(url)
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

    def _get_movie_by_id(self, id, trailer=False, images=False):
        movie = {}
        page = self._load_url(self.url_film + str(id) + '.html')
        soup = BeautifulSoup(page.content, "html.parser")
        exist = soup.find_all("div", {"class": 'z-movie'})
        if exist:
            page = DetailPage(soup)
            movie = self._get_movie_data(page, fa_id=id)
            if trailer:
                trailer_url = self._get_trailer(movie['title'])
                if trailer_url:
                    movie.update({'trailer': trailer_url})
        if images and movie.get('id', False):
            movie.update({'images': self._get_movie_images(movie['id'])})
        return movie

    def _get_movie_by_args(self, key, value, trailer=False, images=False):
        movie = {}
        if key in FIELDS_MOVIE:
            options = '&stype[]=%s' % key
            url = self.url + 'advsearch.php?stext=' + \
                str(value) + options
            page = self._load_url(url)
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
        page = self._load_url(url)
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
        page = self._load_url(url)
        movies = self._return_list_movies(page, 'top_service', top)
        return movies
