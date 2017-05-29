import requests
from bs4 import BeautifulSoup


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
        return float(rating['content'])

    def _get_number_of_votes(self, soup):
        votes = soup.find("span", {"itemprop": 'ratingCount'})
        return int(votes['content'])

    def _get_directors(self, soup):
        directors = []
        directors_cell = soup.find_all("span", {"class": 'director'})
        for director_cell in directors_cell:
            director = director_cell.find("span", {"itemprop": 'name'})
            directors.append(director.get_text())
        return directors

    def _get_actors(self, soup):
        actors = []
        actors_cell = soup.find_all("span", {"itemprop": 'actor'})
        for actor_cell in actors_cell:
            actor = actor_cell.find("span", {"itemprop": 'name'})
            actors.append(actor.get_text())
        return actors

    def _get_poster(self, soup):
        image = soup.find("img", {"itemprop": 'image'})
        return str(image['src'])

    def get_movie(self, id_movie):
        """Return a dictionary with the data of the movie.

        Args:
            id_movie (str, int): Filmaffinity identifier
        Returns:
            TYPE: Dictionary with movie data
        """
        page = requests.get(self.url_film + str(id_movie) + '.html')
        soup = BeautifulSoup(page.text, "html.parser")
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

    def search_movie(self, title):
        options = '&stype=title&orderby=relevance'
        page = requests.get(
            self.url + 'search.php?stext=' + str(title) + options
        )
        soup = BeautifulSoup(page.text, "html.parser")
        movies_cell = soup.find_all("div", {"class": 'movie-card'})
        movies = []
        for movie_cell in movies_cell:
            title = movie_cell.find('div', {'class': 'mc-title'})
            directors = []
            director_cell = movie_cell.find('div', {'class': 'credits'})
            director_cell = director_cell.find('span', {'class': 'nb'})
            directors.append(director_cell.get_text())
            movie = {
                'title': title.get_text() if title else None,
                'directors': directors if directors else None,
                'id': str(movie_cell['data-movie-id']),
            }
            movies.append(movie)
        return movies
