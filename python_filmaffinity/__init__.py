# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

FIELDS_MOVIE = ['title', 'id']
FIELDS_TYPE = ['title', 'director', 'cast']


class Filmaffinity:

    base_url = 'https://www.filmaffinity.com/'

    def __init__(self, lang='es'):
        """Init the search service.

        Args:
            lang (str, optional): Language of the page
        """
        self.lang = lang
        self.url = self.base_url + self.lang + '/'
        self.url_film = self.url + 'film'

    def _get_title(self, soup):
        name_cell = soup.find("span", {"itemprop": 'name'})
        name = name_cell.get_text()
        return name

    def _get_title_by_search(self, soup):
        title = soup.find('div', {'class': 'mc-title'})
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

    def _get_movie_by_id(self, id):
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

        return movie

    def _get_movie_by_args(self, key, value):
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
                movie = self._get_movie_by_id(id)
        return movie

    def get_movie(self, **kwargs):
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
                    movie = self._get_movie_by_id(value)
                else:
                    movie = self._get_movie_by_args(key, value)
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
            soup = BeautifulSoup(page.text, "html.parser")
            movies_cell = soup.find_all("div", {"class": 'movie-card'})
            for cell in movies_cell:
                movie = {
                    'title': self._get_title_by_search(cell),
                    'directors': self._get_directors_by_search(cell),
                    'id': str(cell['data-movie-id']),
                    'poster': self._get_poster_by_search(cell),
                }
                movies.append(movie)
        return movies

    def top_filmaffinity(self, **kwargs):
        """Return a list with the top filmaffinity movies.

        Args:

            from_year: Search from the year
            to_year: Search until the year
        Returns:
            TYPE: Lis with movies data
        """
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
        soup = BeautifulSoup(page.text, "html.parser")
        movies_cell = soup.find_all("div", {"class": 'movie-card'})
        for cell in movies_cell:
            movie = {
                'title': self._get_title_by_search(cell),
                'directors': self._get_directors_by_search(cell),
                'id': str(cell['data-movie-id']),
                'poster': self._get_poster_by_search(cell),
            }
            movies.append(movie)
        return movies

    def top_premieres(self):
        """Return a list with the top filmaffinity movies.

        Args:

            from_year: Search from the year
            to_year: Search until the year
        Returns:
            TYPE: Lis with movies data
        """
        movies = []
        url = self.url + 'topcat_new_th_es.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        movies_cell = soup.find_all("div", {"class": 'movie-card'})
        for cell in movies_cell:
            movie = {
                'title': self._get_title_by_search(cell),
                'directors': self._get_directors_by_search(cell),
                'id': str(cell['data-movie-id']),
                'poster': self._get_poster_by_search(cell),
            }
            movies.append(movie)
        return movies
