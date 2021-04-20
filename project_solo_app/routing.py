# chat/routing.py
from django.urls import re_path

from project_solo_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/status/(?P<status_name>\w+)/$', consumers.StatusConsumer.as_asgi()),
]