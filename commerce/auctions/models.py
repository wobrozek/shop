from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy
from datetime import datetime

class User(AbstractUser, models.Model):
    pass

class Auction(models.Model):

    class CategoryChoices(models.TextChoices):
        FASHION = "FA", gettext_lazy("FASHION")
        TOYS = "TO", gettext_lazy("TOYS")
        ELECTRONICS = "EL", gettext_lazy("ELECTRONICS")
        HOME = "HO", gettext_lazy("HOME")
        CARS = "CR", gettext_lazy("CARS")
    


    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    img = models.CharField(max_length=512, default='none')
    price = models.FloatField()
    category = models.CharField(max_length=2, choices=CategoryChoices.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE ,)
    subscribers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    startDate = models.DateTimeField(auto_now=True)
    endDate = models.DateTimeField()

class Comment(models.Model):
    text = models.CharField(max_length=2048)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment")


class Bid(models.Model):
    price = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid")
