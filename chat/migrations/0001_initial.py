# Generated by Django 4.0.10 on 2025-02-01 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "conversation_type",
                    models.CharField(
                        choices=[
                            ("DIRECT", "Direct"),
                            ("GROUP", "Group"),
                            ("SYSTEM", "System"),
                        ],
                        default="DIRECT",
                        max_length=10,
                    ),
                ),
                (
                    "role_restriction",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ADMIN", "Admin"),
                            ("USER", "User"),
                            ("USER_GIRL", "User Girl"),
                            ("USER_BOY", "User Boy"),
                            ("USER_GIRL_BOY", "User Girl Boy"),
                            ("USER_WOMEN", "User Women"),
                            ("USER_PREGNANT", "User Pregnant"),
                            ("DOCTOR", "Doctor"),
                            ("NURSE", "Nurse"),
                            ("PHARMACIST", "Pharmacist"),
                            ("PHYSICIAN", "Physician"),
                            ("NURSE_MIDWIFE", "Nurse Midwife"),
                            ("HEALTH_EDUCATOR", "Health Educator"),
                            ("HEALTH_ADVISOR", "Health Advisor"),
                            ("HEALTH_CENTER", "Health Center"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_groups",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="conversations", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "conversation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.conversation",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
    ]
