from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("watchlist/", views.watchlist_view, name="watchlist"), 
    path("categories/", views.categories_view, name="categories"),
    path("create/", views.create_view, name="create"),
    path("editProfile/",views.edit_profile_view,name="editProfile"),

    #listing path and forms
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("listing/watchlist/<int:listing_id>", views.add_watchlist_view, name="addWachList"),
]

# filles
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





