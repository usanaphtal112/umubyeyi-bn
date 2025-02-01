from django.db import models
from django.utils import timezone
import uuid
from accounts.models import CustomUser


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=20, choices=[("inbox", "Inbox"), ("group", "Group")]
    )
    name = models.CharField(
        max_length=255, blank=True, null=True
    )  # Optional for groups
    created_at = models.DateTimeField(default=timezone.now)
    participants = models.ManyToManyField(
        CustomUser, related_name="chats", blank=True, through="ChatParticipant"
    )

    def __str__(self):
        return f"{self.type} Chat: {self.name or 'N/A'}"


class ChatParticipant(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    unread_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("chat", "user")

    def __str__(self):
        return f"{self.user.username} in {self.chat}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_messages"
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    read_by = models.ManyToManyField(
        CustomUser, related_name="read_messages", blank=True
    )

    def __str__(self):
        return f"Message from {self.sender.phone_number} to {self.receiver.phone_number}: {self.content[:20]}"
