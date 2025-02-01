from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re as regex

User = get_user_model()


def validate_phonenumber_field(phonenumber):
    if not phonenumber:
        raise serializers.ValidationError({"phonenumber": "This field is required."})
    try:
        # Basic pattern: Only digits, and length between 9 and 15 characters
        phone_pattern = r"^\d{9,10}$"
        if not regex.match(phone_pattern, phonenumber):
            raise serializers.ValidationError(
                {"phonenumber": "Invalid phone number format."}
            )
    except ValidationError:
        raise serializers.ValidationError(
            {"phonenumber": "Enter a valid phone number."}
        )
    return phonenumber


def validate_names(first_name, last_name):
    if not first_name:
        raise serializers.ValidationError({"first_name": "This field is required."})
    if not first_name.isalpha():
        raise serializers.ValidationError(
            {"first_name": "Name should only contain letters."}
        )

    if not last_name:
        raise serializers.ValidationError({"last_name": "This field is required."})
    if not last_name.isalpha():
        raise serializers.ValidationError(
            {"last_name": "Name should only contain letters."}
        )

    return first_name, last_name


def validate_password_fields(password, confirm_password):
    if not password:
        raise serializers.ValidationError({"password": "This field is required."})
    if not confirm_password:
        raise serializers.ValidationError(
            {"confirm_password": "This field is required."}
        )

    if password != confirm_password:
        raise serializers.ValidationError({"password": "Passwords do not match."})

    if len(password) < 8:
        raise serializers.ValidationError(
            {"password": "Password must be at least 8 characters long."}
        )

    if not regex.search(r"^(?=.*[A-Z])(?=.*[a-z]).+$", password):
        raise serializers.ValidationError(
            {"password": "Password must contain at least one small and capital letter."}
        )

    if not regex.search(r".*\d+.*", password):
        raise serializers.ValidationError(
            {"password": "Password must contain at least one numerical value."}
        )

    if not regex.search(r"[!@#$%^&*()_+]", password):
        raise serializers.ValidationError(
            {"password": "Password must contain at least one special character."}
        )

    return password


def is_phonenumber_already_registered(phone_number):
    User = get_user_model()
    return User.objects.filter(phone_number=phone_number).exists()
