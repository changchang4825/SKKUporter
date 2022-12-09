# chat/consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, class_name, sender, message, created_at):
       return Message.objects.create(class_name=class_name, sender=sender, message=message, created_at=created_at)

    async def connect(self):
        self.class_name = self.scope['url_route']['kwargs']['class_name']
        self.class_group_name = 'chat_%s' % self.class_name

        # Join class group
        await self.channel_layer.group_add(
            self.class_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave class group
        await self.channel_layer.group_discard(
            self.class_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        created_at = timezone.now().isoformat()

        new_msg = await self.create_chat(self.class_name, sender, message, created_at)

        # Send message to class group
        await self.channel_layer.group_send(
            self.class_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'created_at': created_at
            }
        )

    # Receive message from class group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        created_at = event['created_at']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'created_at': created_at
        }))