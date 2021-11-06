from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# a list of category choices for creating models and searching them

# Do i add a user_id to each model to keep track of who created what?
# Do i add instances of data with the users username?
# How is the data stored into the user data so only the user can alter the info given? Is that under the user model thats been created in django? Session?

# do I link the auctions listings, bidding, and model library to the user?\
# Link to listings
# Values: Email, Sex, DOB, SSN, Self Description
class User(AbstractUser):
    user_id = models.IntegerField(primary_key=True, unique=True)

# Listing
# Foreign Key: Bids - One to Many One Listing to many bids
# Foreign Key: Comment - Many comments for one listing
class Listing(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    description = models.CharField(max_length=300)
    listing_price = models.FloatField()
    current_bid = models.FloatField(default=0)
    category = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    buyer = models.CharField(max_length=64, default='')
    # listing_id = models.IntegerField(primary_key=True, unique=True)
    user_listing = models.ForeignKey(User, blank=False, on_delete=CASCADE, related_name="user_listing")
    active = models.BooleanField(default=True)

    # do I need primary keys here? How does it know the comments and bids are being listed?
    # user = models.ForeignKey(User, blank=True, on_delete=CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.name}, {self.listing_price}, {self.user_listing}"


# Comment
# Values: Username, Comment, Rating/Vote, CommentAComment, comment_id
# ForeignKey: Links to Bid so the comments are part of the bid
class Comment(models.Model):
    content = models.CharField(max_length=300)
    # comment_id = models.IntegerField(primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    # How can I link the comment?
    # How can I access the comment?
    # Link the comment to the listing
    # 1-to-many relationship
    listing = models.ForeignKey(Listing, blank=True, on_delete=CASCADE, related_name="comment")
    user_comment = models.ForeignKey(User, blank=False, on_delete=CASCADE, related_name="user_comment")

    def __str__(self):
        return f"{self.listing}, {len(self.content)}, {self.user_comment}"

# Bid
# Values: Item of bid, Picture, Starting Bid, Description, Buy Now value, bid_id
class Bid(models.Model):
    bid_price = models.FloatField()
    # bid_id = models.IntegerField(primary_key=True, unique=True) 
    created = models.DateTimeField(auto_now_add=True)
    # Where did the bid come from? 
    # 1-to-many relationship
    listing = models.ForeignKey(Listing, blank=True, on_delete=CASCADE, related_name="bid")
    user_bid = models.ForeignKey(User, blank=False, on_delete=CASCADE, related_name="user_bid")

    def __str__(self):
        return f"{self.bid_price}, {self.listing}, {self.user_bid}"


class Watchlist(models.Model):
    user = ForeignKey(User, blank=False, on_delete=CASCADE, related_name="watchlist_user")
    listing = ForeignKey(Listing, blank=False, on_delete=CASCADE, related_name="watchlist_listing")
    # wathlist_id = models.IntegerField(primary_key=True, unique=True)

    def __str__(self):
        return f"{self.user}, {self.listing}, {self.listing.category}"