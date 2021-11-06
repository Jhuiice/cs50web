from django.urls import path

from . import views


app_name = 'moreModels'

urlpatterns = [
    path('', views.index, name='index')
]