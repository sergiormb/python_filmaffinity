"""Page type: detail."""
from .page import Page


class DetailPage(Page):
    """Page type: detail."""

    def get_title(self):
        """Get the title."""
        name = None
        name_cell = self.soup.find("span", {"itemprop": 'name'})
        if name_cell:
            name = name_cell.get_text()
        return name

    def get_year(self):
        """Get the year."""
        year = None
        year_cell = self.soup.find("dd", {"itemprop": 'datePublished'})
        if year_cell:
            year = year_cell.get_text()
        return year

    def get_description(self):
        """Get the description."""
        description = None
        description_cell = self.soup.find("dd", {"itemprop": 'description'})
        if description_cell:
            description = description_cell.get_text()
        return description

    def get_rating(self):
        """Get the rating."""
        rating = self.soup.find("div", {"id": 'movie-rat-avg'})
        if rating:
            try:
                rating = str(rating['content'])
            except ValueError:
                rating = None
        return rating

    def get_number_of_votes(self):
        """Get the number of votes."""
        votes = self.soup.find("span", {"itemprop": 'ratingCount'})
        if votes:
            try:
                votes = int(votes['content'])
            except ValueError:
                votes = None
        return votes

    def get_actors(self):
        """Get the actors."""
        actors = []
        actors_cell = self.soup.find_all("span", {"itemprop": 'actor'})
        for actor_cell in actors_cell:
            actor = actor_cell.find("span", {"itemprop": 'name'})
            actors.append(actor.get_text())
        return actors

    def get_poster(self):
        """Get the poster."""
        image = self.soup.find("img", {"itemprop": 'image'})
        if image:
            try:
                image = str(image['src'])
            except ValueError:
                image = None
        return image

    def get_directors(self):
        """Get the directors."""
        directors = []
        directors_cell = self.soup.find_all("span", {"class": 'director'})
        for director_cell in directors_cell:
            director = director_cell.find("span", {"itemprop": 'name'})
            directors.append(director.get_text())
        return directors

    def get_duration(self):
        """Get Duration."""
        duration = ''
        dc = self.soup.find("dd", {"itemprop": 'duration'})
        if dc:
            duration = dc.get_text()
        return duration

    def get_country(self):
        """Get the country."""
        country = ''
        dc = self.soup.find("span", {"id": 'country-img'})
        if dc:
            country = dc.img['title']
        return country

    def get_genre(self):
        """Get the genre."""
        genres = []
        dc = self.soup.find("span", {"itemprop": 'genre'})
        if dc:
            [genres.append(i.get_text()) for i in dc.find_all("a")]
        return genres

    def get_awards(self):
        """Get the awards.

        Returns:
            TYPE: List of dicts (dict keys: year, award)
        """
        awards = []
        ac = self.soup.find("dd", {"class": 'award'})
        if not ac:
            return awards
        for i in ac.find_all("a"):
            awards.append({'year': i.get_text(),
                           'award': i.next_sibling[2:]})
        return awards

    def get_reviews(self):
        """Get the critics reviews.

        Returns:
            TYPE: List of dicts (dict keys: author, review, url)
        """
        reviews = []
        for i in self.soup.find_all("div", {"class": 'pro-review'}):
            reviews.append(
                {'author': i.find("div", {
                    "itemprop": 'author'}).get_text(),
                 'review': i.find("div", {
                     "itemprop": 'reviewBody'}).get_text(),
                 'url': i.a['href'] if i.a else None})
        return reviews
