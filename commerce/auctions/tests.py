from urllib import response
from django.test import TestCase
from .models import User
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from http import HTTPStatus

class form(TestCase):

    def test_photo(self):
        us1 = User.objects.create_user("Marian","mail@gmail.com","123456")
        us2 = User.objects.create_user("Szymon", "mail@gmail.com", "123456")
        us3 = User.objects.create_user("Dorota", "mail@gmail.com", "123456")

        self.assertEqual(us1.img, "/profileImg/1.jpg")

    def test_mail(self):
        msg = EmailMessage('Request Callback',
                           'Here is the message.', to=['wobrozek@gmail.com'])
        msg.send()
        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'wobrozek@gmial.com',
        #     ['wojtekb2000wbe@gmail.com'],
        #     fail_silently=False,
        # )






