from django.contrib import admin
from .models import ChatParticipant, Message, Chat


admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(ChatParticipant)
