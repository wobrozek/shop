from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy
from datetime import datetime ,timezone
from PIL import Image,ImageDraw,ImageFont


class User(AbstractUser, models.Model):
    pass
    img = models.ImageField(upload_to='profileImg/',blank=True )

    @classmethod
    def create_user(cls,username,email,password):
        user = cls(username=username,email=email,password=password)
        user.createDefaultImg()
        return user

    def createDefaultImg(self):
        img = Image.new('RGB',(100,100),color=(189, 195, 199))
        ctx= ImageDraw.Draw(img)
        font = ImageFont.truetype(font="arial.ttf",size=50)
        ctx.text((30,25),self.username[0],fill=(44, 62, 80),font=font)
        img.save(f'media/profileImg/{self.id}.jpg')
        self.img=f'media/profileImg/{self.id}.jpg'

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
    img = models.ImageField(upload_to='auctionImg/')
    endDate = models.DateTimeField()
    price = models.FloatField()
    category = models.CharField(max_length=2, choices=CategoryChoices.choices)
    subscribers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    startDate = models.DateTimeField(auto_now=True )
    close=models.BooleanField(default=False)

    def getWinner(self):
        bids = self.bid.all()
        try:
            winnerBid = bids.order_by('-price')[0]
            return winnerBid
        except:
            return None

    def daysLeft(self):
        toEnd = self.endDate-datetime.now(timezone.utc)
        return toEnd.days

class Comment(models.Model):
    text = models.CharField(max_length=2048)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment")


class Bid(models.Model):
    price = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid")