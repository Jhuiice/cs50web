from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from auctions.models import Listing, Bid, Comment, Watchlist
# used for aggregates in finding the highest bidder
from django.db.models import Max
import datetime

from .models import User



# used for creating a listing and showing categories of listings
CATEGORY_CHOICES = (
    ("Motors", "Motors"),
    ("Fashion", "Fashion"),
    ("Electronics", "Electronics"),
    ("Collectibles & Art", "Collectibles & Art"),
    ("Home & Garden", "Home & Garden"),
    ("Sporting Goods", "Sporting Goods"),
    ("Toys", "Toys"),
    ("Miscellaneous", "Miscellaneous")
)
IMAGES = {}

# Forms for views

class CreateListingForm(forms.Form):
    name = forms.CharField(max_length=64, required=True)
    image = forms.ImageField(required=True)
    description = forms.CharField(max_length=500,
        widget=forms.Textarea, 
        required=True)
    listing_price = forms.FloatField(required=True)
    # create hidden inputs in the form with widget=forms.HiddenInput()
    current_bid = forms.FloatField(initial=0, widget=forms.HiddenInput())
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)
    buyer = forms.CharField(initial="", widget=forms.HiddenInput())


# I can access the user right in the html template by the keyword user.
# Authentication that the user is signed in is neccissary too
def get_images():
    listings = Listing.objects.all()
    for listing in listings:
        if listing.id not in IMAGES.keys():
            IMAGES[listing.id] = f"auctions/media/{listing.image}"
    return IMAGES


def index(request):
    listings = Listing.objects.all()
    for listing in listings:
        if listing.id not in IMAGES.keys():
            IMAGES[listing.id] = f"auctions/media/{listing.image}"
    return render(request, 'auctions/index.html', {
        "listings": listings,
        "images": IMAGES
    })

# what if listings have the same names?
# Need listing name and id?
def listing(request, name, id):
    listing = Listing.objects.get(pk=id, name=name)
    comments = Comment.objects.filter(listing=listing).all()
    image = f"auctions/media/{listing.image}"
    error = ''
    if request.method == "POST":

        # Close listing
        if request.POST.get('close'):
            # max bidder
            max_bid = Bid.objects.all().aggregate(Max('bid_price'))
            max_bid = max_bid['bid_price__max']
            bid_winner = Bid.objects.filter(bid_price=max_bid).get()
            bid_winner = bid_winner.user_bid.username
            listing.buyer_username = bid_winner
            listing.active = False
            listing.save()
            bid_winner = Bid.objects.filter(listing=listing)
            error = f'This listing has been closed by {listing.user_listing.username}'
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                'image': image,
                'comments': comments,
                'error': error,
            })

        # Add a comment
        if request.POST.get('comment'):
            content = request.POST["comment"]
            comment = Comment(listing=listing, content=content, user_comment=request.user)
            comment.save()
            return render(request, 'auctions/listing.html', {
            "listing": listing,
            "image": image,
            "comments": comments,
            "error": error,
        })

        # COMPLETE WATCHLIST 
        if request.POST.get("watchlist"):
            # dupliates put a conditional on it
            get_watchlist = Watchlist.objects.filter(user=request.user)
            
            listing = Listing.objects.get(name=name, id=id)
            for watch in get_watchlist:
                if watch.listing == listing:
                    watch.delete()
                    return render(request, 'auctions/listing.html', {
                        "listing": listing,
                        "image": image,
                        "comments": comments,
                        "error": error,
                    })
                
            new_watchlist = Watchlist(user=request.user, listing=listing)
            new_watchlist.save()
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "image": image,
                "comments": comments,
                "error": error,
            })
            
                    

        # create a current bid price instead of overwriting the listing_price
        if request.POST.get('bid'):
            new_bid = float(request.POST["bid"])
            old_bid = float(listing.current_bid)
            listing_price = listing.listing_price
            bid = Bid(bid_price=new_bid, listing=listing, user_bid=request.user)
            bid.save()
            if new_bid > old_bid and new_bid > listing_price:
                listing.current_bid = new_bid
                listing.save()
                return render(request, 'auctions/listing.html', {
                "listing": listing,
                "old_price": old_bid,
                "new_price": new_bid,
                "image": image,
                "comments": comments,
        })
            else:
                error = "Bid must be higher than current bid or listing price"
                return render(request, 'auctions/listing.html', {
                "listing": listing,
                "image": image,
                "comments": comments,
                "error": error,
        })
        return render(request, 'auctions/listing.html', {
        "listing": listing,
        "image": image,
        "comments": comments,
        "error": error,
    })
    else:
        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "image": image,
            "comments": comments,
        })

def watchlist(request):
    user_id = request.user.pk
    user = User.objects.filter(pk=user_id).get()
    # query objects that can be iterated on
    user_watchlist = Watchlist.objects.filter(user=user)
    print(user_watchlist)
    images = get_images()
    return render(request, 'auctions/watchlist.html', {
        "watchlist": user_watchlist,
        'images': images,
    })


def create(request):
    form = CreateListingForm()
    
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.POST.get("image")
        print(image)
        description = request.POST.get("description")
        listing_price = request.POST.get("listing_price")
        current_bid = 0
        category = request.POST.get("category")
        buyer = ''
        user_listing = request.user
        new_listing = Listing(
            name = name,
            image = image,
            description = description,
            listing_price = listing_price,
            current_bid = current_bid,
            category = category,
            buyer = buyer,
            user_listing = user_listing,
        )
        new_listing.save()
        listings = Listing.objects.all()
        for listing in listings:
            if listing.id not in IMAGES.keys():
                IMAGES[listing.id] = f"auctions/media/{listing.image}"
        return render(request, "auctions/index.html", {
            "listings": listings,
            "images": IMAGES
        })
    else:
        return render(request, 'auctions/create.html', {
            "form": form,
        })


def categories(request, category='all'):
    categories = []
    for a_category in CATEGORY_CHOICES:
        categories.append(a_category[1])
    listings = Listing.objects.filter(category=category)
    print(listings, category, categories)
    return render(request, 'auctions/categories.html', {
        'categories': categories,
        'listings': listings
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


def register(request):
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
            # Gives back error after trying to post
            # How do we give the notice on the fly?
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
