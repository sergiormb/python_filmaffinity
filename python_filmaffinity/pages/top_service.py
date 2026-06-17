"""Page type: top_service."""
from .page import Page


class TopServicePage(Page):
    """Page type: top_service."""

    def get_title(self):
        """Get the title."""
        title_cell = self.soup.find('div', {'class': 'mc-right'})
        if title_cell:
            title = title_cell.find('h3')
            if title:
                return title.get_text().strip()
        return super(TopServicePage, self).get_title()
