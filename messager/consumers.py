from channels.generic.websocket import AsyncWebsocketConsumer
import json
class MessagesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_anonymous:
            # 未登录用户拒绝连接
            await self.close()
        else:
            self.channel_layer.group_add(self.scope['user'].username, self.channel_layer)
            await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=json.dumps(text_data))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.scope['user'].username, self.channel_layer)

