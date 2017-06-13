class Page(object):
    """This is a simple python scraping.

    Attributes:
        soup (TYPE): Page analyzed by BeautifulSoup.
    """
    def __init__(self, soup):
        """Init the class.

        Args:
            soup (TYPE): Page analyzed by BeautifulSoup
        """
        self.soup = soup

    def get_title(self):
        """Get title."""
        title = self.soup.find('div', {'class': 'mc-title'})
        return title.get_text() if title else None

    def get_rating(self):
        """Get rating."""
        rating = self.soup.find("div", {"class": 'avg-rating'})
        if rating:
            try:
                rating = float(rating.get_text())
            except ValueError:
                rating = rating.get_text()
        return rating

    def get_directors(self):
        """Get directors."""
        directors = []
        director_cell = self.soup.find('div', {'class': 'credits'})
        if director_cell:
            director_cell = director_cell.find('span', {'class': 'nb'})
            directors.append(director_cell.get_text())
        return directors if directors else None

    def get_poster(self):
        """Get poster."""
        poster_img = None
        poster = self.soup.find('div', {'class': 'mc-poster'})
        if poster:
            poster_img = poster.find('img')
            poster_img = poster_img['src']
        return poster_img
