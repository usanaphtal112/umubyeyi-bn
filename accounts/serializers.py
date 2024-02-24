from rest_framework import serializers
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
