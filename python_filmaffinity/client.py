"""Client."""
# -*- coding: utf-8 -*-

import requests
import random
from functools import partial
from cachetools import cached, hashkey

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
from bs4 import BeautifulSoup
from .config import cache, FIELDS_MOVIE
from .pages import DetailPage, SearchPage, TopPage, TopServicePage


class Client:
    """Client to make requests to Filmaffinity."""

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

    def _get_trailer(self, title):
        title += ' trailer'
        title = quote(title)
        page = requests.get(self.url_youtube + str(title))
        soup = BeautifulSoup(page.text, "html.parser")
        vid = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]
        return 'https://www.youtube.com' + vid['href']

    @cached(cache, key=partial(hashkey, id))
    def _get_movie_by_id(self, id, trailer=False):
        movie = {}
        page = requests.get(self.url_film + str(id) + '.html')
        soup = BeautifulSoup(page.text, "html.parser")
        exist = soup.find_all("div", {"class": 'z-movie'})
        if exist:
            page = DetailPage(soup)
            movie = {
                'id': id,
                'title': page.get_title(),
                'year': page.get_year(),
                'rating': page.get_rating(),
                'votes': page.get_number_of_votes(),
                'description': page.get_description(),
                'directors': page.get_directors(),
                'actors': page.get_actors(),
                'poster': page.get_poster(),
            }
            if trailer:
                movie.update({'trailer': self._get_trailer(movie['title'])})

        return movie

    def _get_movie_by_args(self, key, value, trailer=False):
        movie = {}
        if key in FIELDS_MOVIE:
            options = '&stype[]=%s' % key
            url = self.url + 'advsearch.php?stext=' + \
                str(value) + options
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            movies_cell = soup.find_all("div", {"class": 'movie-card-1'})
            if movies_cell:
                cell = movies_cell[0]
                id = str(cell['data-movie-id'])
                movie = self._get_movie_by_id(id, 'search')
        return movie

    def _return_list_movies(self, page, method, top=10):
        movies = []
        soup = BeautifulSoup(page.text, "html.parser")
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
            movies_cell = soup.find_all("div", {"class": 'movie-card'})
            class_ = TopServicePage
        for cell in movies_cell[:top]:
            page = class_(cell)
            movie = {
                'title': page.get_title(),
                'directors': page.get_directors(),
                'id': page.get_id(),
                'poster': page.get_poster(),
                'rating': page.get_rating(),
            }
            movies.append(movie)
        return movies

    def _recommend(self, service, trailer=False):
        movie = {}
        if self.lang == 'es':
            url = self.url + 'topcat.php?id=' + service
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            movies_cell = soup.find_all("div", {"class": 'movie-card'})
            cell = random.choice(movies_cell)
            id = str(cell['data-movie-id'])
            movie = self._get_movie_by_id(id, trailer)
        return movie

    def _top_service(self, top, service):
        movies = []
        if self.lang == 'es':
            top = 40 if top > 40 else top
            url = self.url + 'topcat.php?id=' + service
            page = requests.get(url)
            movies = self._return_list_movies(page, 'top_service', top)
        return movies
