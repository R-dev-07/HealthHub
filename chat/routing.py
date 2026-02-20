import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket Consumer for chat"""
    
    async def connect(self):
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.chat_room_group_name = f'chat_{self.chat_room_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.chat_room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message', '')
        user = self.scope['user']
        
        if message_content.strip():
            # Save message to database
            await self.save_message(message_content, user)
            
            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'username': user.get_full_name(),
                    'user_id': user.id,
                    'timestamp': timezone.now().isoformat(),
                }
            )
    
    async def chat_message(self, event):
        """Handle incoming message from group"""
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp'],
        }))
    
    @database_sync_to_async
    def save_message(self, content, user):
        """Save message to database"""
        try:
            chat_room = ChatRoom.objects.get(id=self.chat_room_id)
            Message.objects.create(
                chat_room=chat_room,
                sender=user,
                content=content,
                message_type='text'
            )
            chat_room.last_message_at = timezone.now()
            chat_room.save()
        except ChatRoom.DoesNotExist:
            pass
