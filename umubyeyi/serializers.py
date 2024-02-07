from rest_framework import serializers
from .models import LastMenstrualPeriod


class LastMenstrualPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastMenstrualPeriod
        fields = ("last_menstrual_period",)


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastMenstrualPeriod
        fields = (
            "last_menstrual_period",
            "current_date",
            "days_pregnant",
            "weeks_pregnant",
            "trimester",
            "expected_date_delivery",
        )
