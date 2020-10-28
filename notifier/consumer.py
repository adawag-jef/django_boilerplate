from channels.generic.websocket import AsyncJsonWebsocketConsumer


class Consumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notif", self.channel_name)
        print(f"Added {self.channel_name} channel to notif")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notif", self.channel_name)
        print(f"Removed {self.channel_name} channel to notif")

    async def user_notif_create(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")

    async def user_notif_update(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")

    async def profile_notif_update(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")

    async def profile_notif_create(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")

# self.scope['url_route']['kwargs']['ch_name']
