from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/mosque/<int:mosque_id>/', consumers.MosqueNotificationsConsumer.as_asgi()),
]
