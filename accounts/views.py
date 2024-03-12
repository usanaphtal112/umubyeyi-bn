from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    CustomUserSerializers,
    UserLoginSerializers,
    UserRoleSerializers,
    RetrieveUserSerializer,
)
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

        # Check if phone number is already taken
        if get_user_model().objects.filter(phonenumber=phonenumber).exists():
            return Response(
                {"error": "Phone Number already used."}, status=status.HTTP_409_CONFLICT
            )

        # Create the user After validation
        User = get_user_model()
        User.objects.create_user(
            phonenumber=phonenumber,
            password=data.get("password"),
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


@extend_schema(
    description="User Sign-In (Login) Endpoint",
    tags=["Users"],
)
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            phonenumber_error = e.detail.get("phonenumber")
            password_error = e.detail.get("password")

            if phonenumber_error:
                return Response(
                    {"error": "Phone Number Must not be blank."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if password_error:
                return Response(
                    {"error": "Password must not be blank."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        phonenumber = serializer.validated_data["phonenumber"]
        password = serializer.validated_data["password"]

        # Validate user inputs
        if UserRegistrationValidator.validate_phone_number(phonenumber):
            return Response(
                {"error": "Phone Number or Password is incorrect. Please try again."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if UserRegistrationValidator.validate_password_field(password, password):
            return Response(
                {"error": "Phone Number or Password is incorrect. Please try again."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = authenticate(
            request,
            phonenumber=phonenumber,
            password=password,
        )
        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                "access_token": str(refresh.access_token),
                # "user": CustomUserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Phone Number or Password is incorrect. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@extend_schema(
    description="List of Health Advisor Users",
    tags=["Users"],
)
class HealthAdvisorListView(generics.ListAPIView):
    serializer_class = RetrieveUserSerializer

    def get_queryset(self):
        role_name = "Health Advisor"  # to be adjusted
        queryset = RetrieveUserSerializer.filter_by_role(role_name)
        return queryset

    def handle_exception(self, exc):
        if isinstance(exc, serializers.ValidationError):
            # Return the custom error response
            return Response({"detail": exc.detail}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
