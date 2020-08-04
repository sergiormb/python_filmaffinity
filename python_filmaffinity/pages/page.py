import re

pattern_title_year = re.compile(
    '(.+[^0-9|^(|^\[])[([|\[| |.|_]*(19\d\d|20\d\d)[)|\]]?', re.IGNORECASE)

classifications = [
    'Documentary',
    'Animation',
    'Tv Series',
    'TV Miniseries',
]


class Page(object):
    """This is a simple python scraping object that represents
    all possible data that we can scrap from a FilmAffinity detail page.
    Most of the scraping for this class is based on tags from the
    top searches (the most used in this module).
    Some of the results will return nothing, depending if the scrapped page
    contains the corresponding data. Some specific data are implemented
    into his own subclass (Ex: get_awards and get_reviews are implemented
    into DetailPage because those fields only are in detail page)

    Attributes:
        soup (TYPE): Page analyzed by BeautifulSoup.
    """
    def __init__(self, soup):
        """Init the class.

        Args:
            soup (TYPE): Page analyzed by BeautifulSoup
        """
        self.soup = soup

    def get_id(self):
        """Get the id."""
        cell = self.soup.find('div', {'class': 'movie-card'})
        if not cell:
            return None
        return cell.get('data-movie-id', None)

    def get_title(self):
        """Get title."""
        title = self.soup.find('div', {'class': 'mc-title'})
        return title.get_text() if title else None

    def get_rating(self):
        """Get rating."""
        cell = self.soup.find(
            "div", {"class": ['avg-rating', 'avgrat-box']})
        if cell:
            try:
                cell = float(cell.get_text())
            except ValueError:
                cell = cell.get_text()
        return cell

    def get_directors(self):
        """Get directors."""
        director_cell = self.soup.find(
            'div', {'class': ['director', 'mc-director']})
        if not director_cell:
            return []
        cell = director_cell.find_all('span', {'class': 'nb'})
        # Sometimes the FilmAffinity classification
        # appears inside a directors tag, so we filter it
        if not cell:
            return None
        return [
            i.a['title'] for i in cell if i.a['title'] not in classifications
        ]

    def get_actors(self):
        """Get the actors."""
        actors_cell = self.soup.find(
            'div', {'class': ['cast', 'mc-cast']})
        if not actors_cell:
            return None
        cell = actors_cell.find_all("span", {'class': 'nb'})
        # Sometimes the  FilmAffinity classification
        # appears inside a actors tag, so we filter it
        if not cell:
            return None
        try:
            return [
                i.a['title'] for i in cell if i.a['title'] not in classifications
            ] if cell else None
        except:
            return None

    def get_poster(self):
        """Get poster."""
        poster_img = None
        poster = self.soup.find('div', {'class': 'mc-poster'})
        if poster:
            poster_img = poster.find('img')
            poster_img = poster_img['src']
        return poster_img

    def get_duration(self):
        """Get Duration."""
        cell = self.soup.find('div', {'class': 'duration'})
        return cell.get_text().strip() if cell else None

    def get_year(self):
        """Get the year."""
        cell = self.soup.find('div', {'class': 'mc-data'})
        return cell.find_all('div')[0].get_text() if cell else self._get_year_from_title()

    def _get_year_from_title(self):
        """Get the year from title."""
        # Sometimes we cannot find the year inside specific tag,
        # so...we try to guess from the title
        t = self.get_title()
        re_match = pattern_title_year.match(t if t else '')
        return re_match.group(2) if re_match else None

    def get_country(self):
        """Get the country."""
        cell = self.soup.find('div', {'class': ['mc-data', 'mc-title']})
        if not cell:
            return None
        return cell.img['title']

    def get_genre(self):
        """Get the genre."""
        cell = self.soup.find('div', {'class': 'mc-data'})
        return cell.find('a', {'class': 'genre'}).get_text() if cell else None

    def get_description(self):
        """Get the description."""
        cell = self.soup.find('div', {'class': 'mc-data'})
        return cell.find('a', {'class': 'synop-text'}).get_text() if cell else None

    def get_number_of_votes(self):
        """Get the number of votes."""
        cell = self.soup.find("div", {"class": ['rat-count', 'ratcount-box']})
        return cell.get_text().strip() if cell else None

    def get_awards(self):
        """Get the awards."""
        # Implemented into subclass: see DetailPage for more details
        return []

    def get_reviews(self):
        """Get the reviews."""
        # Implemented into subclass: see DetailPage for more details
        return []
