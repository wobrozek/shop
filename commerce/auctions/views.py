from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AuctionForm, BidForm ,CommentForm ,EditProfileForm
from django.contrib import messages
from PIL import ImageDraw,Image

from .models import User, Auction, Bid ,Comment
from .tasks import send_mails


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
        form = AuctionForm(request.POST,request.FILES)
        if form.is_valid():
            aukcja = form.save(commit=False)
            aukcja.author = request.user
            aukcja.save()

            
            return HttpResponseRedirect(f"/listing/{aukcja.id}")
        else:
            return render(request,"auctions/form.html",{
                "form":form,
                "formValue":"Create",
                "formTitle":"Create Listing",
            })

    else:
        form = AuctionForm
        return render(request, "auctions/form.html",{
        "form":form,
        "formValue": "Create",
        "formTitle": "Create Listing",
    })

def create_contex(listing_id,request):
    formBid = BidForm(request.POST)
    formComments =CommentForm(request.POST)
    auction = Auction.objects.get(id=listing_id)

    #auction is still active ?
    if auction.close == False and auction.endDate < datetime.now(auction.endDate.tzinfo):
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
        oferts = Bid.objects.select_related().filter(auction=auction)
    except Bid.DoesNotExist:
        oferts = []
        
    #auctions have a comments ?
    try:
        comments=auction.comment.select_related()
    except:
        comments=[]

    #user is subscriber of auction ?
    if request.user in auction.subscribers.all():
        follow=True
    else:
        follow=False

    return {"auction":auction,"historyBid":oferts,
            "formBid":formBid,"formComments":formComments,
            "message":"","owner":owner,"follow":follow,
            "close":auction.close,"winnerBid":winnerBid,
            "comments":comments}


@login_required
def add_watchlist_view(request,listing_id):
    auction=Auction.objects.get(id=listing_id)

    if request.user in auction.subscribers.all():
        auction.subscribers.remove(request.user)
    else:
        auction.subscribers.add(request.user)

    return JsonResponse({'watchList':request.user.watchlist.all().count()}, status=200)


def listing_view(request,listing_id):
    context=create_contex(listing_id,request)

    if request.method=="POST":

        #if user is the owner he can only close the auction
        if context["owner"]==True:
            context["auction"].close=True
            context["auction"].save()
            context["close"]=True
            print(context)
            return render(request, "auctions/listing.html", context)

        # if user is not owner and place a bid
        if context["formBid"].is_valid():

            #if wrong price
            if context["formBid"].cleaned_data.get('price')<=context["auction"].price:
                context["message"]="the price must be greater than previous bid"
                return render(request, "auctions/listing.html",context)

            bid =context["formBid"].save(commit=False)
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

@login_required
def edit_profile_view(request):
    if request.method=="POST":
        form=EditProfileForm(request.POST,request.FILES,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect(reverse('index'))

    form=EditProfileForm(instance=request.user)
    return render(request,"auctions/form.html",{
        "form":form,
        "formTitle":"Edit Profile",
        "formValue":"Edit"
    })


def auction_img(request,auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if auction is not None:
        return render(request,"auction/index.html", {'img':auction.img})
