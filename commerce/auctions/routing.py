from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path("ws/comments",consumers.commentConsumer,name="comments"),
    path("ws/history/",consumers.HistoryConsumer.as_asgi())
]