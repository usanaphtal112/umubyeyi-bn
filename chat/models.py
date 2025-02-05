from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid

User = get_user_model()


class Conversation(models.Model):
    class ConversationType(models.TextChoices):
        DIRECT = "DIRECT", "Direct"
        GROUP = "GROUP", "Group"
        SYSTEM = "SYSTEM", "System"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_groups"
    )
    conversation_type = models.CharField(
        max_length=10, choices=ConversationType.choices, default=ConversationType.DIRECT
    )
    role_restriction = models.CharField(
        max_length=20, choices=User.Role.choices, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.conversation_type == "GROUP" and not self.role_restriction:
            raise ValidationError("Group conversations must have a role restriction")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
