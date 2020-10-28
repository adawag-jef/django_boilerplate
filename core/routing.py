from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifier.consumer import Consumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("notifications/<ch_name>/", Consumer),
    ])
})
