# Generated by Django 5.0 on 2024-02-07 11:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "umubyeyi",
            "0003_rename_start_date_lastmenstrualperiod_last_menstrual_period",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="lastmenstrualperiod",
            name="trimester",
            field=models.IntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(3),
                ],
            ),
            preserve_default=False,
        ),
    ]
