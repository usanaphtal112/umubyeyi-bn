from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="Real time chat endpoints",
    tags=["Chats"],
)
class MessageHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recipient_id = self.kwargs["recipient_id"]
        queryset = Message.objects.filter(
            sender=user, receiver_id=recipient_id
        ) | Message.objects.filter(sender_id=recipient_id, receiver=user)
        return queryset
