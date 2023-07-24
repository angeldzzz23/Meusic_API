# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from channels.auth import AuthMiddlewareStack

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', AuthMiddlewareStack(consumers.ChatConsumer.as_asgi())),
    re_path(r'ws/chat/$', AuthMiddlewareStack(consumers.ChatConsumer.as_asgi())),
    # re_path(r'ws/chat$', AuthMiddlewareStack(consumers.ChatConsumer.as_asgi())),
]


