from .page import Page


class TopServicePage(Page):

    def get_id(self):
        return self.soup.get('data-movie-id', None)

    def get_title(self):
        title_cell = self.soup.find('div', {'class': 'mc-right'})
        title = title_cell.find('h3')
        return title.get_text() if title else None
