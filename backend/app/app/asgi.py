import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from user.services.notification.consumers import NotificationConsumer
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),  # ✅ ASGI application for HTTP requests
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        path("notifications/<str:room_name>/", NotificationConsumer.as_asgi()),

                    ]
                )
            )
        ),
    }
)
