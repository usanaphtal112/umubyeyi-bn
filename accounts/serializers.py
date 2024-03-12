from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import Role


class CustomUserSerializers(serializers.Serializer):
    phonenumber = serializers.CharField(max_length=10)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class UserRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserLoginSerializers(serializers.Serializer):
    phonenumber = serializers.CharField()
    password = serializers.CharField(write_only=True)


from rest_framework import serializers
from .models import CustomUser


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "firstname",
            "lastname",
            "phonenumber",
            "role",
        ]

    @staticmethod
    def filter_by_role(role_name):
        try:
            # Fetch the role object by name using get()
            role = Role.objects.get(name=role_name)
            # Filter users by the fetched role
            return CustomUser.objects.filter(role=role)
        except Role.DoesNotExist:
            # Raise a specific exception if role is not found
            raise NotFound(detail="The requested role is not available.")
