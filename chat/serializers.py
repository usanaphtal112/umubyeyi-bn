from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .utils import create_role_group

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp"]

    def get_sender(self, obj):
        return {
            "id": str(obj.sender.id),
            "phone_number": str(obj.sender.phone_number),
        }


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    role_restriction = serializers.CharField(read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "conversation_type",
            "role_restriction",
            "messages",
        ]

    def create(self, validated_data):
        # Add the creator to the participants list
        user = self.context["request"].user
        participants = validated_data.pop("participants", [])
        participants.append(user)

        # Create the conversation
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)

        return conversation


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = []

    def create(self, validated_data):
        user = self.context["request"].user
        return create_role_group(user, user.role)
