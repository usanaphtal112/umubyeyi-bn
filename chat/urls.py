from django.urls import path
from .views import (
    ConversationList,
    HealthAdvisorConversation,
    ConversationMessageList,
    DirectConversationAPIView,
    ConversationParticipantAPIView,
)

urlpatterns = [
    path("conversations/", ConversationList.as_view(), name="conversation-list"),
    path(
        "conversations/direct/<uuid:user_id>/",
        DirectConversationAPIView.as_view(),
        name="get-or-create-direct-conversation",
    ),
    path(
        "conversations/health-advisor/<uuid:advisor_id>/",
        HealthAdvisorConversation.as_view(),
        name="health-advisor-conversation",
    ),
    path(
        "conversations/<uuid:conversation_id>/participant/",
        ConversationParticipantAPIView.as_view(),
        name="conversation-participantd",
    ),
    path(
        "messages/<uuid:conversation_id>/",
        ConversationMessageList.as_view(),
        name="conversation-messages",
    ),
]
