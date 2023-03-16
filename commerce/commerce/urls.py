from django.contrib import admin
from django.urls import include, path

from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("", include("auctions.urls")),
]



