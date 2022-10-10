from urllib import response
from django.test import TestCase

from http import HTTPStatus

class form(TestCase):
    def test_happy_path(self):
        response = self.client.post("/create", data={"title":"klapki", "description":"lorem"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
