from rest_framework import serializers

from .models import Role


class CustomUserSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    phonenumber = serializers.CharField(max_length=10)
    # email = serializers.EmailField()
    firstname = serializers.CharField(max_length=150)
    lastname = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class UserRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserLoginSerializers(serializers.Serializer):
    phonenumber = serializers.CharField()
    password = serializers.CharField(write_only=True)
