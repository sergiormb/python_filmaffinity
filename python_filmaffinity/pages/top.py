from .page import Page


class TopPage(Page):

    def get_id(self):
        movie = self.soup.find("div", {"class": 'movie-card'})
        return str(movie.get('data-movie-id')) if movie else None
