import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, phonenumber, email=None, password=None, **extra_fields):
        if not phonenumber:
            raise ValueError("The phonenumber field must be set")
        email = self.normalize_email(email) if email else None
        username = phonenumber
        user = self.model(
            phonenumber=phonenumber, email=email, username=username, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phonenumber, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phonenumber, email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    phonenumber = models.CharField(max_length=10, unique=True)

    is_profile_updated = models.BooleanField(default=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=225, blank=True, null=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Add any additional fields you need

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phonenumber


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
