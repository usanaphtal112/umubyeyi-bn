# chat/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Conversation
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_health_advisor_inbox(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.HEALTH_ADVISOR:
        # Create system conversation for health advisor
        conversation = Conversation.objects.create(
            conversation_type=Conversation.ConversationType.SYSTEM,
            role_restriction=User.Role.HEALTH_ADVISOR,
        )
        conversation.participants.add(instance)
