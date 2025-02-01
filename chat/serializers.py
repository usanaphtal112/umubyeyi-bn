from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(source="id")
    content = serializers.CharField()
    sender = serializers.CharField(source="sender.phonenumber")
    receiver = serializers.CharField(source="receiver.phonenumber")
    chat = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    read_by = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Message
        fields = [
            "message_id",
            "content",
            "sender",
            "receiver",
            "chat",
            "created_at",
            "read_by",
        ]
