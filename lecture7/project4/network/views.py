from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

import json

from .models import User, Profile, Posts


def index(request):

    # load all the posts here and send it to the template
    all_posts = Posts.objects.all()
    # what we need
    # photo and username

    return render(request, "network/index.html",
                  {
                      "posts": all_posts
                  })


def edit_post(request, id):
    try:
        post = Posts.objects.get(post_id=id)
    except:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        post.content = data.content
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT response Required"
        })


@ensure_csrf_cookie
@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status="400")
    content = request.POST.get("content")
    # data = json.loads(request.body)
    # content = data['content']
    # # # render in data from json fetch request
    user = request.user

    # # create post in data base to be fetched
    post = Posts.objects.create(content=content, user=user)
    post.save()
    posts = Posts.objects.all()
    # TODO order in reverse chronological order (newest first)
    # json will render the single page resoonse
    return render(request, "network/index.html", {
        "posts": posts
    })


def profile(request, username):
    user = User.objects.filter(username=username).get()
    profile = Profile.objects.filter(name=username).get()
    # new accounts will have no posts
    try:
        posts = Posts.objects.filter(user=user)
    except:
        posts = None
    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": posts,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and profile
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            # create a profile upon creation of user
            profile = Profile.objects.create(
                name=user.username,
                user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
