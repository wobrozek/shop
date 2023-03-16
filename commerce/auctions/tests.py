from urllib import response
from django.test import TestCase
from .models import User

from http import HTTPStatus

class form(TestCase):

    def test_photo(self):
        us1 = User.objects.create_user("Marian","mail@gmail.com","123456")
        us2 = User.objects.create_user("Szymon", "mail@gmail.com", "123456")
        us3 = User.objects.create_user("Dorota", "mail@gmail.com", "123456")

        us1.createDefaultImg()

        self.assertEqual(us1.img, "media/profileImg/1.jpg")


