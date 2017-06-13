"""Page type: search."""
from .page import Page


class SearchPage(Page):
    """Page type: search."""

    def get_id(self):
        """Get the id."""
        return str(self.soup['data-movie-id'])

    def get_rating(self):
        """Get rating."""
        rating = self.soup.find("div", {"class": 'avgrat-box'})
        if rating:
            try:
                rating = str(rating.get_text())
            except ValueError:
                rating = rating.get_text()
        return rating
