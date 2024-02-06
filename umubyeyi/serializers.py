from rest_framework import serializers
from .models import LastMenstrualPeriod


class LastMenstrualPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastMenstrualPeriod
        fields = (
            "start_date",
            "current_date",
            "days_pregnant",
            "weeks_pregnant",
            "expected_date_delivery",
        )
