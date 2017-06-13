from .page import Page


class DetailPage(Page):

    def get_title(self):
        name_cell = self.soup.find("span", {"itemprop": 'name'})
        name = name_cell.get_text()
        return name

    def get_year(self):
        year_cell = self.soup.find("dd", {"itemprop": 'datePublished'})
        year = year_cell.get_text()
        return year

    def get_description(self):
        description_cell = self.soup.find("dd", {"itemprop": 'description'})
        description = description_cell.get_text()
        return description

    def get_rating(self):
        rating = self.soup.find("div", {"id": 'movie-rat-avg'})
        if rating:
            try:
                rating = str(rating['content'])
            except ValueError:
                rating = None
        return rating

    def get_number_of_votes(self):
        votes = self.soup.find("span", {"itemprop": 'ratingCount'})
        if votes:
            try:
                votes = int(votes['content'])
            except ValueError:
                votes = None
        return votes

    def get_actors(self):
        actors = []
        actors_cell = self.soup.find_all("span", {"itemprop": 'actor'})
        for actor_cell in actors_cell:
            actor = actor_cell.find("span", {"itemprop": 'name'})
            actors.append(actor.get_text())
        return actors

    def get_poster(self):
        image = self.soup.find("img", {"itemprop": 'image'})
        if image:
            try:
                image = str(image['src'])
            except ValueError:
                image = None
        return image

    def get_directors(self):
        directors = []
        directors_cell = self.soup.find_all("span", {"class": 'director'})
        for director_cell in directors_cell:
            director = director_cell.find("span", {"itemprop": 'name'})
            directors.append(director.get_text())
        return directors
