"""Page type: search."""
from .page import Page


class SearchPage(Page):
    """Page type: search."""

    def get_id(self):
        """Get the id."""
        return str(self.soup['data-movie-id'])
