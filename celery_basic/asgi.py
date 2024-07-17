"""
ASGI config for celery_basic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from celery_basic_app.consumer import TaskStatusConsumer
from image_formats_conversion.consumer import TaskImageConversion

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_basic.settings")

# application = get_asgi_application()

websocket_urlpattern = [
  path("ws/celery_basic/", TaskStatusConsumer.as_asgi()),
  path("ws/image_conversion/", TaskImageConversion.as_asgi())
]

application = ProtocolTypeRouter({
  "http" : get_asgi_application(),
  "websocket" : URLRouter(websocket_urlpattern)
})