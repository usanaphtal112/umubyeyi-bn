from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation_type",
        "role_restriction",
        "created_by",
        "created_at",
        "updated_at",
    )
    list_filter = ("conversation_type", "role_restriction")
    search_fields = ("id", "created_by__username")
    readonly_fields = ("id", "created_at", "updated_at")
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "content", "timestamp")
    list_filter = ("timestamp", "sender")
    search_fields = ("content", "sender__username")
    readonly_fields = ("id", "timestamp")
