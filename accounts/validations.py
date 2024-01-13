# validation_utils.py
import re as regex

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.response import Response


class UserRegistrationValidator:
    @staticmethod
    def validate_email_field(email):
        if not email:
            return Response(
                {"error": "Email cannot be blank."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST
            )

        return None

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number:
            return Response(
                {"error": "Phone number cannot be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Basic pattern: Only digits, and length between 9 and 15 characters
        phone_pattern = r"^\d{9,15}$"
        if not regex.match(phone_pattern, phone_number):
            return Response(
                {"error": "Invalid phone number format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @staticmethod
    def validate_name(firstname, lastname):
        if not firstname:
            return Response(
                {"error": "First Name can not be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not lastname:
            return Response(
                {"error": "Last name can not be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @staticmethod
    def validate_password_field(password, confirm_password):
        if not password:
            return Response(
                {"error": "Password cannot be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not confirm_password:
            return Response(
                {"error": "Confirm Password cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirm_password:
            return Response(
                {"error": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        character_pattern = r"^(?=.*[A-Z])(?=.*[a-z]).+$"
        if not regex.search(character_pattern, password):
            return Response(
                {
                    "error": "Password must contain at least one small and capital letter."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        number_pattern = r".*\d+.*"
        if not regex.search(number_pattern, password):
            return Response(
                {"error": "Password must contain at least one numerical value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not regex.search(r"[!@#$%^&*()_+]", password):
            return Response(
                {"error": "Password must contain at least one special character."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @staticmethod
    def validate_username_field(username):
        if not username:
            return Response(
                {"error": "Username cannot be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(username) < 6:
            return Response(
                {"error": "Username should be at least 6 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @staticmethod
    def is_email_already_registered(email):
        User = get_user_model()
        return User.objects.filter(email=email).exists()

    @staticmethod
    def is_username_already_taken(username):
        User = get_user_model()
        return User.objects.filter(username=username).exists()

    @staticmethod
    def validate_user_registration_data(data):
        # email = data.get("email")
        phonenumber = data.get("phonenumber")
        username = data.get("username")
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # email_error = UserRegistrationValidator.validate_email_field(email)
        # if email_error:
        #     return email_error

        phonenumber_error = UserRegistrationValidator.validate_phone_number(phonenumber)
        if phonenumber_error:
            return phonenumber_error

        username_error = UserRegistrationValidator.validate_username_field(username)
        if username_error:
            return username_error

        name_error = UserRegistrationValidator.validate_name(firstname, lastname)
        if name_error:
            return name_error

        password_error = UserRegistrationValidator.validate_password_field(
            password, confirm_password
        )
        if password_error:
            return password_error
        return None
