from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
import uuid

User = get_user_model()


class ConversationList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Chat"],
        description="List all conversations for the authenticated user",
        responses={200: ConversationSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Example response",
                value=[
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "participants": ["user1_id", "user2_id"],
                        "conversation_type": "DIRECT",
                        "messages": [],
                    }
                ],
            )
        ],
    )
    def get(self, request):
        conversations = request.user.conversations.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Chat"],
        description="Create a new conversation",
        request=ConversationSerializer,
        examples=[
            OpenApiExample(
                "Create conversation example",
                value={"participants": ["user2_id"], "conversation_type": "DIRECT"},
                request_only=True,
            )
        ],
        responses={
            201: ConversationSerializer,
            400: OpenApiResponse(description="Invalid input"),
        },
    )
    def post(self, request):
        serializer = ConversationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DirectConversationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Chat"],
        description="Check if a direct conversation exists with the specified user",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="ID of the user to check conversation with",
                required=True,
                type=uuid.UUID,
            )
        ],
        responses={
            200: ConversationSerializer,
            404: OpenApiResponse(description="No conversation found"),
        },
    )
    def get(self, request, user_id):
        try:
            other_user = User.objects.get(id=user_id)
            conversation = (
                Conversation.objects.filter(
                    conversation_type=Conversation.ConversationType.DIRECT,
                    participants=request.user,
                )
                .filter(participants=other_user)
                .first()
            )

            if conversation:
                serializer = ConversationSerializer(conversation)
                return Response(serializer.data)
            return Response(
                {"detail": "No conversation found"}, status=status.HTTP_404_NOT_FOUND
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        tags=["Chat"],
        description="Create a new direct conversation with the specified user",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="ID of the user to create conversation with",
                required=True,
                type=uuid.UUID,
            )
        ],
        responses={
            201: ConversationSerializer,
            400: OpenApiResponse(
                description="Invalid request or conversation already exists"
            ),
            404: OpenApiResponse(description="User not found"),
        },
    )
    def post(self, request, user_id):
        try:
            other_user = User.objects.get(id=user_id)

            # Check if conversation already exists
            existing_conversation = (
                Conversation.objects.filter(
                    conversation_type=Conversation.ConversationType.DIRECT,
                    participants=request.user,
                )
                .filter(participants=other_user)
                .exists()
            )

            if existing_conversation:
                return Response(
                    {"detail": "Conversation already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new direct conversation
            conversation = Conversation.objects.create(
                conversation_type=Conversation.ConversationType.DIRECT,
                created_by=request.user,
            )
            conversation.participants.add(request.user, other_user)

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class HealthAdvisorConversation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Chat"],
        description="Check if a conversation exists with a Health Advisor",
        parameters=[
            OpenApiParameter(
                name="advisor_id",
                description="ID of the Health Advisor to check conversation with",
                required=True,
                type=uuid.UUID,
            )
        ],
        responses={
            200: ConversationSerializer,
            403: OpenApiResponse(description="User is not a Health Advisor"),
            404: OpenApiResponse(description="No conversation found"),
        },
    )
    def get(self, request, advisor_id):
        try:
            advisor = User.objects.get(id=advisor_id)

            # Verify the user is a Health Advisor
            if advisor.role != User.Role.HEALTH_ADVISOR:
                return Response(
                    {"detail": "Specified user is not a Health Advisor"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            conversation = (
                Conversation.objects.filter(
                    conversation_type=Conversation.ConversationType.DIRECT,
                    participants=request.user,
                )
                .filter(participants=advisor)
                .first()
            )

            if conversation:
                serializer = ConversationSerializer(conversation)
                return Response(serializer.data)
            return Response(
                {"detail": "No conversation found"}, status=status.HTTP_404_NOT_FOUND
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "Health Advisor not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        tags=["Chat"],
        description="Create a new conversation with a Health Advisor",
        parameters=[
            OpenApiParameter(
                name="advisor_id",
                description="ID of the Health Advisor to create conversation with",
                required=True,
                type=uuid.UUID,
            )
        ],
        responses={
            201: ConversationSerializer,
            400: OpenApiResponse(
                description="Invalid request or conversation already exists"
            ),
            403: OpenApiResponse(description="User is not a Health Advisor"),
            404: OpenApiResponse(description="Health Advisor not found"),
        },
    )
    def post(self, request, advisor_id):
        try:
            advisor = User.objects.get(id=advisor_id)

            # Verify the user is a Health Advisor
            if advisor.role != User.Role.HEALTH_ADVISOR:
                return Response(
                    {"detail": "Specified user is not a Health Advisor"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Check if conversation already exists
            existing_conversation = (
                Conversation.objects.filter(
                    conversation_type=Conversation.ConversationType.DIRECT,
                    participants=request.user,
                )
                .filter(participants=advisor)
                .exists()
            )

            if existing_conversation:
                return Response(
                    {"detail": "Conversation already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new health advisor conversation
            conversation = Conversation.objects.create(
                conversation_type=Conversation.ConversationType.DIRECT,
                created_by=request.user,
            )
            conversation.participants.add(request.user, advisor)

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response(
                {"detail": "Health Advisor not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ConversationMessageList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Chat"],
        description="List all messages in a specific conversation",
        parameters=[
            OpenApiParameter(
                name="conversation_id",
                description="ID of the conversation",
                required=True,
                type=uuid.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: MessageSerializer(many=True),
            403: OpenApiResponse(
                description="User is not a participant in this conversation"
            ),
            404: OpenApiResponse(description="Conversation not found"),
        },
    )
    def get(self, request, conversation_id):
        try:
            # Get conversation and verify user is a participant
            conversation = Conversation.objects.get(id=conversation_id)
            if request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not a participant in this conversation"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            messages = Message.objects.filter(conversation=conversation).order_by(
                "timestamp"
            )
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        tags=["Chat"],
        description="Send a new message in a specific conversation",
        parameters=[
            OpenApiParameter(
                name="conversation_id",
                description="ID of the conversation",
                required=True,
                type=uuid.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=MessageSerializer,
        examples=[
            OpenApiExample(
                "Send message example",
                value={
                    "content": "Hello, how can I help?",
                },
                request_only=True,
            )
        ],
        responses={
            201: MessageSerializer,
            400: OpenApiResponse(description="Invalid message data"),
            403: OpenApiResponse(
                description="User is not a participant in this conversation"
            ),
            404: OpenApiResponse(description="Conversation not found"),
        },
    )
    def post(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not a participant in this conversation"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Add conversation to the request data
            data = request.data.copy()
            data["conversation"] = conversation_id

            serializer = MessageSerializer(data=data, context={"request": request})
            if serializer.is_valid():
                serializer.save(sender=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )
