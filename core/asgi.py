"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from home.consumers import *
from channels.auth import AuthMiddlewareStack


django_asgi_app  = get_asgi_application()


ws_patterns = [
    path('ws/test/', TestConsumer.as_asgi()), 
    path('ws/async/', AsyncTestConsumer.as_asgi())
]


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack( URLRouter(ws_patterns))}
)
