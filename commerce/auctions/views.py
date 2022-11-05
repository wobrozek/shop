from datetime import datetime
from email import message
from multiprocessing import context
from turtle import title
from unicodedata import category
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AuctionForm, BidForm
from django.forms import ValidationError

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
def create_view(request):
    if request.method=="POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            aukcja = form.save(commit=False)
            aukcja.author = request.user
            aukcja.save()
            
            return HttpResponseRedirect(f"/listing/{aukcja.id}")
        else:
            return render(request,"auctions/create.html",{
                "form":form
            })

    else:
        form = AuctionForm
        return render(request, "auctions/create.html",{
        "form":form
    })

def create_contex(listing_id,request):
    form = BidForm(request.POST)
    auction = Auction.objects.get(id=listing_id)

    #auction is still active ?
    if auction.endDate < datetime.now(auction.endDate.tzinfo):
        auction.close=True
        auction.save()

    #if closed add the winer
    winnerBid=""
    if auction.close == True:
        winnerBid=auction.getWinner()

    #user is a author ?
    if auction.author == request.user:
        owner=True
    else:
        owner=False

    #auctions have bids ?
    try:
        oferts = Bid.objects.filter(auction=auction)
    except Bid.DoesNotExist:
        oferts = []

    #user is subscriber of auction ?
    if request.user in auction.subscribers.all():
        follow=True
    else:
        follow=False

    return {"auction":auction,"historyBid":oferts,"form":form,"message":"","owner":owner,"follow":follow,"close":auction.close,"winnerBid":winnerBid}


@login_required
def add_watchlist_view(request,listing_id):
    context=create_contex(listing_id,request)

    if request.method=="POST":
        if context["follow"]:
            context["auction"].subscribers.remove(request.user)
        else:
            context["auction"].subscribers.add(request.user)

    return HttpResponseRedirect(f"/listing/{context['auction'].id}")

def listing_view(request,listing_id):
    context=create_contex(listing_id,request)

    if request.method=="POST":

        #if user is the owner he can only close the auction
        if context["owner"]==True:
            context["auction"].close=True
            context["auction"].save()
            return render(request, "auctions/listing.html", context)

        # if user is not owner and place a bid
        if context["form"].is_valid():
            if context["form"].cleaned_data.get('price')<=context["auction"].price:
                context["message"]="the price must be greater than previous bid"
                return render(request, "auctions/listing.html",context)
            bid =context["form"].save(commit=False)
            bid.auction=context["auction"]
            bid.author=request.user
            context["auction"].price=bid.price
            bid.save()
            context["auction"].save()
            HttpResponseRedirect(f"/listing/{context['auction'].id}")
        else:
            return render(request, "auctions/listing.html",context)

    return render(request, "auctions/listing.html",context)


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
