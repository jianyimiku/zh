from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from messager.consumers import MessagesConsumer
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator  ## 防止通过websocket进行csrf攻击
application = ({
    'websocket': AllowedHostsOriginValidator(
AuthMiddlewareStack(
        URLRouter([
            path('ws/<str:username>/', MessagesConsumer)
            ])
        )
    )
})