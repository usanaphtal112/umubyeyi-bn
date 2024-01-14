from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import CustomUserSerializers, UserRoleSerializers
from .validations import UserRegistrationValidator


@extend_schema(
    description="User Registration Endpoint",
    tags=["Users"],
)
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializers

    def post(self, request):
        data = request.data
        validation_response = UserRegistrationValidator.validate_user_registration_data(
            data
        )

        if validation_response:
            return validation_response

        phonenumber = data.get("phonenumber")
        username = data.get("username")

        if UserRegistrationValidator.validate_phone_number(phonenumber):
            return Response(
                {"error": "Phone Number already used."}, status=status.HTTP_409_CONFLICT
            )

        if UserRegistrationValidator.is_username_already_taken(username):
            return Response(
                {"error": "Username already taken."}, status=status.HTTP_409_CONFLICT
            )

        # Create the user After validation
        User = get_user_model()
        User.objects.create_user(
            phonenumber=phonenumber,
            username=username,
            password=data.get("password"),
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
        )
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


@extend_schema(
    description="Create role endpoint",
    tags=["Users"],
)
class CreateUserRoleAPIView(generics.CreateAPIView):
    serializer_class = UserRoleSerializers

    def post(self, request, *args, **kwargs):
        serializer = UserRoleSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
