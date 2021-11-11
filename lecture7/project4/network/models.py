from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from datetime import datetime
from django.db.models.expressions import Case
from django.utils import timezone


class User(AbstractUser):
    pass

    # def __str__(self):
    #     return f"User: {AbstractUser.username}"

# TODO: Finish implementing following and followers into the database


# class Followers(models.Model):
#     user = models.ForeignKey(User, on_delete=CASCADE)
    # follower = models.


# class Following(models.Model):
#     following = models.BooleanField(default=False)
#     followers = models.BooleanField(default=False)

# TODO on registration of a new account a Profile must be auto made and autolinked to the user this will be in the views


class Profile(models.Model):
    """
    The specific content of the user includes Bio, Photo, Background Photo
    PK: user_id, username, followers, following
    """

    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=256, blank=True)
    # TODO change the settings to save the photos to network/static/media/img
    photo = models.ImageField(
        default="./media/network/img/default_user_photo.jpg")
    background_photo = models.ImageField(
        default="./media/network/img/black_background.jpg")
    # following = models.ForeignKey(Following, on_delete=SET_NULL)
    user = models.ForeignKey(User, on_delete=CASCADE)
    profile_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Profile name: {self.name}"


class Posts(models.Model):
    """User created Posts Model linked through the profile"""

    post_id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=256)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    # post must reference the profile that is creating it
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"User: {self.user.username}, Content: {self.content[:50]}"
