from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import Role
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .validations import (
    validate_names,
    validate_password_fields,
    validate_phonenumber_field,
)

User = get_user_model()


class CustomUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        # Validate phone number first
        phone_number = validate_phonenumber_field(data.get("phone_number"))

        # Then validate names
        first_name, last_name = validate_names(
            data.get("first_name"), data.get("last_name")
        )

        # Finally validate password
        password = validate_password_fields(
            data.get("password"), data.get("confirm_password")
        )

        # Return validated data
        return {
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "confirm_password": data.get("confirm_password"),
        }


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        # Validate phone number
        phone_number = validate_phonenumber_field(data.get("phone_number"))

        # Validate password
        password = validate_password_fields(data.get("password"), data.get("password"))

        return {"phone_number": phone_number, "password": password}


class UserRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserLoginSerializers(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "role",
        ]

    @staticmethod
    def filter_by_role(role_name):
        try:
            # Fetch the role object by name using get()
            role = Role.objects.get(name=role_name)
            # Filter users by the fetched role
            return User.objects.filter(role=role)
        except Role.DoesNotExist:
            # Raise a specific exception if role is not found
            raise NotFound(detail="The requested role is not available.")
