from django.urls import path
from .views import MessageHistoryView

urlpatterns = [
    path(
        "history/<uuid:recipient_id>/",
        MessageHistoryView.as_view(),
        name="chat-history",
    ),
]
