# Generated by Django 5.0 on 2024-02-07 10:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("umubyeyi", "0002_lastmenstrualperiod_expected_date_delivery"),
    ]

    operations = [
        migrations.RenameField(
            model_name="lastmenstrualperiod",
            old_name="start_date",
            new_name="last_menstrual_period",
        ),
    ]
