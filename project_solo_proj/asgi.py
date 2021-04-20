"""
ASGI config for project_solo_proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
from tasks import consumers

import project_solo_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_solo_proj.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            project_solo_app.routing.websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({
        "background-tasks": consumers.BackgroundTaskConsumer.as_asgi()
    }),
})