from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    img = models.CharField(max_length=512, blank=True)

class Comment(models.Model):
    text = models.CharField(max_length=2048)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment")

class Bid(models.Model):
    price = models.FloatField()
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    auction = models.ForeignKey(Auction ,on_delete=models.CASCADE, related_name="bid")