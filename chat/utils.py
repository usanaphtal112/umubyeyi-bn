from django.core.exceptions import PermissionDenied
from .models import Conversation


def create_role_group(user, role):
    if user.role != role:
        raise PermissionDenied("You can only create groups for your own role")

    group = Conversation.objects.create(
        conversation_type=Conversation.ConversationType.GROUP,
        role_restriction=role,
        created_by=user,
    )
    group.participants.add(user)
    return group


def join_role_group(user, group_id):
    group = Conversation.objects.get(id=group_id)
    if user.role != group.role_restriction:
        raise PermissionDenied("You can't join this group")
    group.participants.add(user)
    return group
