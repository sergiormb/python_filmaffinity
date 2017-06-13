class Page(object):

    def __init__(self, soup):
        self.soup = soup

    def get_title(self):
        title = self.soup.find('div', {'class': 'mc-title'})
        return title.get_text() if title else None

    def get_rating(self):
        rating = self.soup.find("div", {"class": 'avg-rating'})
        if rating:
            try:
                rating = float(rating.get_text())
            except ValueError:
                rating = rating.get_text()
        return rating

    def get_directors(self):
        directors = []
        director_cell = self.soup.find('div', {'class': 'credits'})
        if director_cell:
            director_cell = director_cell.find('span', {'class': 'nb'})
            directors.append(director_cell.get_text())
        return directors if directors else None

    def get_poster(self):
        poster_img = None
        poster = self.soup.find('div', {'class': 'mc-poster'})
        if poster:
            poster_img = poster.find('img')
            poster_img = poster_img['src']
        return poster_img
