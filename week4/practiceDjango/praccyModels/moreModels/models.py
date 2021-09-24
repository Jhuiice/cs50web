from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
# can i make a table with all the keys relating to one listing?

class User(models.Model):
    key = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}, {self.key}"



class Bid(models.Model):
    name = models.CharField(max_length=64)
    bid_price = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    name = models.CharField(max_length=64)
    # comment = models.ForeignKey(Listing, on_delete=CASCADE, )

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    user_name = models.ForeignKey(User, on_delete=CASCADE, blank=True, related_name="user_name")
    bid = models.ForeignKey(Bid, on_delete=CASCADE, blank=True, related_name="bid")

    def __str__(self):
        return f"{self.name} connection is {self.main_model}"
