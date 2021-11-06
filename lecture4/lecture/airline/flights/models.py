from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

# airport is the through table
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    
    # creates origin_id
    origin = models.ForeignKey(Airport, on_delete=CASCADE, related_name="departures")
    
    # creates destination_id
    destination = models.ForeignKey(Airport, on_delete=CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"


# many to many model
# Why?
# there can be many flights one passenger can take and many passengers that take one flight
class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"