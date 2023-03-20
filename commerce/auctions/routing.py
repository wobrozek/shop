from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path("ws/comments",consumers.commentConsumer,name="comments"),
    path("ws/history/<int:listing_id>",consumers.HistoryConsumer.as_asgi())
]