import json
from channels.generic.websocket import AsyncWebsocketConsumer


class WhatsAppConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = 'whatsapp_admin'

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    # Manejador de eventos enviados al grupo desde las vistas
    async def whatsapp_event(self, event):
        await self.send(text_data=json.dumps(event['data']))
