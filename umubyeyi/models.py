from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from .calculations import Pregnancy


class LastMenstrualPeriod(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_menstrual_period = models.DateField()
    current_date = models.DateField(default=datetime.now)
    days_pregnant = models.IntegerField(blank=True, null=True)
    weeks_pregnant = models.FloatField(blank=True, null=True)
    trimester = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    expected_date_delivery = models.DateField(blank=True, null=True)

    def update_pregnancy_info(self):
        # Update the current date to the actual current date
        self.current_date = datetime.now().date()

        # Calculate pregnancy info using Pregnancy class
        (
            expected_date_delivery,
            weeks_of_pregnancy,
            days_of_pregnancy,
            trimester,
        ) = Pregnancy.calculate_pregnancy_info(self.last_menstrual_period)

        # Update model fields
        self.days_pregnant = days_of_pregnancy
        self.weeks_pregnant = weeks_of_pregnancy
        self.expected_date_delivery = expected_date_delivery
        self.trimester = trimester

    def save(self, *args, **kwargs):
        # Call the update_pregnancy_info method before saving
        self.update_pregnancy_info()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Last Menstrual Period on {self.last_menstrual_period}, Current Date: {self.current_date}"
