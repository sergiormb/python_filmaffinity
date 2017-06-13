"""Page type: top."""
from .page import Page


class TopPage(Page):
    """Page type: top."""

    def get_id(self):
        """Get the id."""
        movie = self.soup.find("div", {"class": 'movie-card'})
        return str(movie.get('data-movie-id')) if movie else None
