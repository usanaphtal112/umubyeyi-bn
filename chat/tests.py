from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Conversation

User = get_user_model()


class ChatTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(phone_number="1234567890", role=User.Role.USER)
        self.user2 = User.objects.create(
            phone_number="0987654321", role=User.Role.HEALTH_ADVISOR
        )

    def test_group_creation(self):
        self.client.force_login(self.user1)
        response = self.client.post("/api/chat/conversations/create_group/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_health_advisor_inbox(self):
        self.client.force_login(self.user2)
        response = self.client.get("/api/v1/chat/conversations/health_advisor_inbox/")
        self.assertEqual(response.status_code, 200)
