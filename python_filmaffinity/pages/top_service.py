"""Page type: top_service."""
from .page import Page


class TopServicePage(Page):
    """Page type: top_service."""

    def get_id(self):
        """Get the id."""
        return self.soup.get('data-movie-id', None)

    def get_title(self):
        """Get the title."""
        title_cell = self.soup.find('div', {'class': 'mc-right'})
        title = title_cell.find('h3')
        return title.get_text() if title else None
