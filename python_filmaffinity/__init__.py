import requests
from bs4 import BeautifulSoup


class Filmaffinity:
        base_url = 'https://www.filmaffinity.com/'

    def __init__(self, lang='es'):
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

    def get_movie(self, id_movie):
        page = requests.get(self.url_film + str(id_movie) + '.html')
        soup = BeautifulSoup(page.content, "html.parser")
        movie = {
            'title': self._get_title(soup),
            'year': self._get_year(soup),
            'rating': self._get_rating(soup),
            'votes': self._get_number_of_votes(soup),
            'description': self._get_description(soup),
        }

        return movie
