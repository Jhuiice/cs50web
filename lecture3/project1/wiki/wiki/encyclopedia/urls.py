from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("<str:title>/edit/", views.edit, name="edit"),
]
