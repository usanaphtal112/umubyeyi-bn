import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        USER_GIRL = "USER_GIRL", "User Girl"
        USER_BOY = "USER_BOY", "User Boy"
        USER_GIRL_BOY = "USER_GIRL_BOY", "User Girl Boy"
        USER_WOMEN = "USER_WOMEN", "User Women"
        USER_PREGNANT = "USER_PREGNANT", "User Pregnant"
        DOCTOR = "DOCTOR", "Doctor"
        NURSE = "NURSE", "Nurse"
        PHARMACIST = "PHARMACIST", "Pharmacist"
        PHYSICIAN = "PHYSICIAN", "Physician"
        NURSE_MIDWIFE = "NURSE_MIDWIFE", "Nurse Midwife"
        HEALTH_EDUCATOR = "HEALTH_EDUCATOR", "Health Educator"
        HEALTH_ADVISOR = "HEALTH_ADVISOR", "Health Advisor"
        HEALTH_CENTER = "HEALTH_CENTER", "Health Center"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=10, unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    is_profile_updated = models.BooleanField(default=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=225, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Add any additional fields you need

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Blacklisted Token (Created: {self.blacklisted_at})"
