# Generated by Django 4.0.10 on 2025-02-05 06:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_delete_role_alter_customuser_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlacklistedToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=500, unique=True)),
                (
                    "blacklisted_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
    ]
