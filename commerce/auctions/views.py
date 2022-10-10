from datetime import datetime
from email import message
from turtle import title
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bid


def index(request):
    return render(request, "auctions/index.html",{
        "auctions": Auction.objects.all()
    })


@login_required
def watchlist_view(request):
    return render(request, "auctions/index.html",{
        "auctions": request.user.watchlist.all()
    })

def categories_view(request):
    return render(request, "auctions/categories.html",{
        "categories": Auction.CategoryChoices.labels       
    })


@login_required
def create_view(reqest):
    if reqest.method=="POST":
        title=reqest.POST["title"]
        description=reqest.POST["description"]
        img=reqest.POST["img"]

        #check if date is in the future
        endDate=datetime.strptime(reqest.POST["endDate"],"%Y-%m-%dT%H:%M")
        if endDate < datetime.now():
            return render(reqest, "auctions/create.html",{
            "message":"The end of auction date must be in the future",
            "categories": Auction.CategoryChoices.labels
            })

        price=int(reqest.POST["price"])
        #check if price is positiv number
        if price < 0:
            return render(reqest, "auctions/create.html",{
            "message":"The price must be greater than zero",
            "categories": Auction.CategoryChoices.labels
            })
        category=reqest.POST["category"]

        try:
            aukcja = Auction.objects.create(author=reqest.user,title=title,description=description,img=img,endDate=endDate,price=price,category=category)
            aukcja.save()
        except IntegrityError:
            render(reqest, "auctions/create.html",{
                "message":"All required field must be",
                "categories": Auction.CategoryChoices.labels
            })
        return HttpResponseRedirect(f"listing/{aukcja.id}")


    else:
        return render(reqest, "auctions/create.html",{
        "categories": Auction.CategoryChoices.labels
    })


def listing_view(reqest,listing_id):
    aukcja =Auction.objects.get(id=listing_id)
    try:
        oferty=Bid.objects.get(auction=aukcja)
    except Bid.DoesNotExist:
        oferty=[]

    return render(reqest, "auctions/listing.html",{
        "auction": aukcja,
        "historyBid":oferty
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
