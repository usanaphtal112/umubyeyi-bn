from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            # Step 1: Get user from authentication middleware
            self.user = self.scope["user"]

            # Step 2: Reject anonymous users immediately
            if self.user.is_anonymous:
                await self.close(
                    code=4001
                )  # Custom close code for authentication failure
                return

            # Step 3: Get conversation ID from URL parameters
            self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

            # Step 4: Fetch conversation and validate participation
            self.conversation = await self.get_conversation()
            if not await self.validate_participation():
                await self.close(code=4003)  # Custom close code for permission denied
                return

            # Step 5: Add to conversation group and accept connection
            await self.channel_layer.group_add(
                str(self.conversation_id), self.channel_name
            )
            await self.accept()

        except (InvalidToken, TokenError) as e:
            await self.close(code=4001)
        except Conversation.DoesNotExist:
            await self.close(code=4004)  # Custom close code for invalid conversation
        except Exception as e:
            await self.close(code=4000)  # Generic error code

    @database_sync_to_async
    def get_conversation(self):
        return Conversation.objects.get(id=self.conversation_id)

    @database_sync_to_async
    def validate_participation(self):
        # Direct conversation check
        if self.conversation.conversation_type == "DIRECT":
            return self.conversation.participants.filter(id=self.user.id).exists()

        # Group conversation check
        if self.conversation.conversation_type == "GROUP":
            return self.user.role == self.conversation.role_restriction

        # System conversation (HEALTH_ADVISOR) check
        if self.conversation.conversation_type == "SYSTEM":
            return self.user.role == User.Role.HEALTH_ADVISOR.value  # Note .value here

        return False

    async def receive_json(self, content):
        try:
            # Step 1: Validate message content
            message_text = content.get("message")
            if not message_text:
                return

            # Step 2: Create and save message
            message = await self.create_message(message_text)

            # Step 3: Broadcast to conversation group
            await self.channel_layer.group_send(
                str(self.conversation_id),
                {
                    "type": "chat.message",
                    "message": {
                        "id": str(message.id),
                        "sender": {
                            "id": str(message.sender.id),
                            "phone_number": str(message.sender.phone_number),
                        },
                        "content": message.content,
                        "timestamp": message.timestamp.isoformat(),
                    },
                },
            )

        except Exception as e:
            pass

    @database_sync_to_async
    def create_message(self, content):
        return Message.objects.create(
            conversation=self.conversation, sender=self.user, content=content
        )

    async def chat_message(self, event):
        await self.send_json(event["message"])
