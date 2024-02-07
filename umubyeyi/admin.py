from django.contrib import admin
from .models import LastMenstrualPeriod


@admin.register(LastMenstrualPeriod)
class LastMenstrualPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "last_menstrual_period",
        "current_date",
        "days_pregnant",
        "weeks_pregnant",
        "trimester",
        "expected_date_delivery",
    )
