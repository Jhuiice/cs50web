from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:name>/<int:id>/", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("create/", views.create, name="create"),
    path("categories/<str:category>", views.categories, name='categories')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)