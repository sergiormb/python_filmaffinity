from unittest import TestCase

import python_filmaffinity


class TestApi(TestCase):
    service = python_filmaffinity.Filmaffinity()

    def test_search(self):
        movie = self.service.get_movie('197671')
        self.assertEqual(movie['title'], 'Piratas del Caribe: La venganza de Salazar')
