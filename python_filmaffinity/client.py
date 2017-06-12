# -*- coding: utf-8 -*-
import requests
import random
import urllib
from bs4 import BeautifulSoup
from .config import FIELDS_MOVIE


class Client:
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

    def _get_title(self, soup):
        name_cell = soup.find("span", {"itemprop": 'name'})
        name = name_cell.get_text()
        return name

    def _get_title_by_search(self, soup):
        title = soup.find('div', {'class': 'mc-title'})
        return title.get_text() if title else None

    def _get_title_by_top(self, soup):
        title_cell = soup.find('div', {'class': 'mc-right'})
        title = title_cell.find('h3')
        return title.get_text() if title else None

    def _get_year(self, soup):
        year_cell = soup.find("dd", {"itemprop": 'datePublished'})
        year = year_cell.get_text()
        return year

    def _get_description(self, soup):
        description_cell = soup.find("dd", {"itemprop": 'description'})
        description = description_cell.get_text()
        return description

    def _get_rating(self, soup):
        rating = soup.find("div", {"id": 'movie-rat-avg'})
        if rating:
            try:
                rating = float(rating['content'])
            except ValueError:
                rating = None
        return rating

    def _get_rating_by_search(self, soup):
        rating = soup.find("div", {"class": 'avg-rating'})
        if rating:
            try:
                rating = float(rating.get_text())
            except ValueError:
                rating = rating.get_text()
        return rating

    def _get_trailer(self, title):
        title += ' trailer'
        title = urllib.quote(title)
        page = requests.get(self.url_youtube + str(title))
        soup = BeautifulSoup(page.text, "html.parser")
        vid = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]
        return 'https://www.youtube.com' + vid['href']

    def _get_number_of_votes(self, soup):
        votes = soup.find("span", {"itemprop": 'ratingCount'})
        if votes:
            try:
                votes = int(votes['content'])
            except ValueError:
                votes = None
        return votes

    def _get_directors(self, soup):
        directors = []
        directors_cell = soup.find_all("span", {"class": 'director'})
        for director_cell in directors_cell:
            director = director_cell.find("span", {"itemprop": 'name'})
            directors.append(director.get_text())
        return directors

    def _get_directors_by_search(self, soup):
        directors = []
        director_cell = soup.find('div', {'class': 'credits'})
        director_cell = director_cell.find('span', {'class': 'nb'})
        directors.append(director_cell.get_text())
        return directors if directors else None

    def _get_actors(self, soup):
        actors = []
        actors_cell = soup.find_all("span", {"itemprop": 'actor'})
        for actor_cell in actors_cell:
            actor = actor_cell.find("span", {"itemprop": 'name'})
            actors.append(actor.get_text())
        return actors

    def _get_poster(self, soup):
        image = soup.find("img", {"itemprop": 'image'})
        if image:
            try:
                image = str(image['src'])
            except ValueError:
                image = None
        return image

    def _get_poster_by_search(self, soup):
        poster = soup.find('div', {'class': 'mc-poster'})
        poster_img = poster.find('img')
        return poster_img['src']

    def _get_movie_by_id(self, id, trailer=False):
        movie = {}
        page = requests.get(self.url_film + str(id) + '.html')
        soup = BeautifulSoup(page.text, "html.parser")
        exist = soup.find_all("div", {"class": 'z-movie'})
        if exist:
            movie = {
                'title': self._get_title(soup),
                'year': self._get_year(soup),
                'rating': self._get_rating(soup),
                'votes': self._get_number_of_votes(soup),
                'description': self._get_description(soup),
                'directors': self._get_directors(soup),
                'actors': self._get_actors(soup),
                'poster': self._get_poster(soup),
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
                movie = self._get_movie_by_id(id, trailer)
        return movie

    def _return_list_movies(self, page, top=10, from_search=False):
        movies = []
        soup = BeautifulSoup(page.text, "html.parser")
        movies_cell = soup.find_all("div", {"class": 'movie-card'})
        for cell in movies_cell[:top]:
            movie = {
                'title': self._get_title_by_top(cell) if not from_search else self._get_title_by_search(cell),
                'directors': self._get_directors_by_search(cell),
                'id': str(cell['data-movie-id']),
                'poster': self._get_poster_by_search(cell),
                'rating': self._get_rating_by_search(cell),
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
            movies = self._return_list_movies(page, top)
        return movies
