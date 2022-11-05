from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("watchlist/", views.watchlist_view, name="watchlist"), 
    path("categories/", views.categories_view, name="categories"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("create/", views.create_view, name="create"),
    path("listing/watchlist/<int:listing_id>", views.add_watchlist_view, name="addWachList"),

]
