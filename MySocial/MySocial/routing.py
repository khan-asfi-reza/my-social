from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

# from Chat.consumers import OnlineOfflineConsumer, InboxConsumer, MessageConsumer, GetOnlineConsumer

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    # path('ws/status/', OnlineOfflineConsumer),
                    # path('ws/inbox/', InboxConsumer),
                    # path('ws/chat/<username>/', MessageConsumer),
                    # re_path('ws/onlineusers/', GetOnlineConsumer),
                ]
            )
        ),
    }
)
