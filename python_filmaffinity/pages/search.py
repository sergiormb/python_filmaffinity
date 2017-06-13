from .page import Page


class SearchPage(Page):

    def get_id(self):
        return str(self.soup['data-movie-id'])

    def get_rating(self):
        rating = self.soup.find("div", {"class": 'avgrat-box'})
        if rating:
            try:
                rating = str(rating.get_text())
            except ValueError:
                rating = rating.get_text()
        return rating