from django.contrib import admin
from .models import LastMenstrualPeriod


@admin.register(LastMenstrualPeriod)
class LastMenstrualPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "start_date",
        "current_date",
        "days_pregnant",
        "weeks_pregnant",
        "expected_date_delivery",
    )
