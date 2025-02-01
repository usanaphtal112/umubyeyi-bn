from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, ChatParticipant, Message
from accounts.models import CustomUser
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        message_type = message_data.get("type")
        message_text = message_data.get("text")
        sender_id = message_data.get("sender_id")
        recipient_id = message_data.get("recipient_id")

        if message_text and sender_id and recipient_id:
            # Check if a chat already exists between the sender and recipient
            chat = await self.get_or_create_chat(sender_id, recipient_id)

            # Create the ChatParticipant instances for sender and recipient
            await self.get_or_create_chat_participants(chat, sender_id, recipient_id)

            # Create the Message instance
            await self.create_message(message_text, sender_id, chat, recipient_id)

            # Send the message to each participant's interface
            participants = await self.get_chat_participants(chat)
            # Convert QuerySet to list or use asyncio.to_thread to iterate over it
            for participant in participants:
                await self.send_message(participant.id, message_data)

    @database_sync_to_async
    def get_or_create_chat(self, sender_id, recipient_id):
        # Your existing logic to get or create a chat
        chat = (
            Chat.objects.filter(participants__id=sender_id)
            .filter(participants__id=recipient_id)
            .first()
        )
        if not chat:
            chat = Chat.objects.create(type="inbox")
            chat.participants.add(sender_id, recipient_id)
            chat.save()
        return chat

    @database_sync_to_async
    def get_or_create_chat_participants(self, chat, sender_id, recipient_id):
        # Your existing logic to get or create chat participants
        sender_participant, _ = ChatParticipant.objects.get_or_create(
            chat=chat, user_id=sender_id
        )
        recipient_participant, _ = ChatParticipant.objects.get_or_create(
            chat=chat, user_id=recipient_id
        )

    @database_sync_to_async
    def create_message(self, message_text, sender_id, chat, recipient_id):
        # Your existing logic to create a message
        sender = CustomUser.objects.get(id=sender_id)
        recipient = CustomUser.objects.get(id=recipient_id)
        return Message.objects.create(
            content=message_text, sender=sender, receiver=recipient, chat=chat
        )

    @database_sync_to_async
    def get_chat_participants(self, chat):
        # Retrieve chat participants asynchronously
        return list(chat.participants.all())

    async def send_message(self, recipient_id, message_data):
        # Send the received message data to the WebSocket client
        await self.send(text_data=json.dumps(message_data))
