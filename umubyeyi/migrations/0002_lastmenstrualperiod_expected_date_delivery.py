# Generated by Django 5.0 on 2024-02-05 22:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("umubyeyi", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lastmenstrualperiod",
            name="expected_date_delivery",
            field=models.DateField(blank=True, null=True),
        ),
    ]