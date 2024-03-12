import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        message_type = message_data["type"]
        message_text = message_data["text"]
        sender_id = message_data["sender_id"]
        chat_id = message_data["chat_id"]

        # Create the message object
        message = Message.objects.create(
            content=message_text, sender_id=sender_id, chat_id=chat_id
        )

        # Get the chat participants excluding the sender
        participants = Chat.objects.get(id=chat_id).participants.exclude(id=sender_id)

        # Send the message to each participant's interface
        for participant in participants:
            await self.send_message(participant.id, message_data)

    async def send_message(self, recipient_id, message_data):
        # Send the message data to the WebSocket client identified by recipient_id
        await self.channel_layer.group_send(
            f"user_{recipient_id}",
            {
                "type": "chat.message",
                "message_data": message_data,
            },
        )

    async def chat_message(self, event):
        # Send the received message data to the WebSocket client
        await self.send(text_data=json.dumps(event["message_data"]))
