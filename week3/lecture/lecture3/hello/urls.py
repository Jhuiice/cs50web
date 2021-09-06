from django.urls import path

from . import views

# app_name is used to prevent template/static collision errors
# and to import the url into the django template language without hardcoding
app_name = "hello"

urlpatterns = [
    path("", views.index, name='index'),
    path("<str:name>", views.greet, name='greet')
]