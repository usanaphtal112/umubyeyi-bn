from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    CustomUserSerializer,
    UserLoginSerializers,
    UserRoleSerializers,
    RetrieveUserSerializer,
)
from .validations import (
    is_phonenumber_already_registered,
)


@extend_schema(
    description="Register a new user account",
    tags=["Authentication"],
    request=CustomUserSerializer,
    responses={
        201: OpenApiResponse(
            description="User registered successfully",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={"message": "User registered successfully"},
                )
            ],
        ),
        400: OpenApiResponse(description="Invalid input data"),
        409: OpenApiResponse(description="Phone number already registered"),
    },
    examples=[
        OpenApiExample(
            "Valid Registration",
            value={
                "phone_number": "+250700000000",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123",
                "confirm_password": "securepassword123",
            },
            request_only=True,
        )
    ],
)
class RegisterAPIView(APIView):
    """API endpoint for user registration."""

    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Database check only after all validations pass
        phone_number = serializer.validated_data["phone_number"]
        if is_phonenumber_already_registered(phone_number):
            return Response(
                {"phone_number": "This phone number is already registered."},
                status=status.HTTP_409_CONFLICT,
            )

        # Create user
        User = get_user_model()
        User.objects.create_user(
            phone_number=phone_number,
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            password=serializer.validated_data["password"],
        )
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


@extend_schema(
    description="Authenticate user and retrieve access token",
    tags=["Authentication"],
    request=UserLoginSerializers,
    responses={
        200: OpenApiResponse(
            description="Login successful",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={"access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."},
                )
            ],
        ),
        401: OpenApiResponse(description="Invalid credentials"),
        400: OpenApiResponse(description="Invalid input data"),
    },
    examples=[
        OpenApiExample(
            "Valid Login",
            value={"phone_number": "+250700000000", "password": "yourpassword"},
            request_only=True,
        )
    ],
)
class LoginAPIView(APIView):
    """API endpoint for user login."""

    serializer_class = UserLoginSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Validate credentials and get user
        try:
            user = authenticate(
                request=request,
                phone_number=serializer.validated_data["phone_number"],
                password=serializer.validated_data["password"],
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token
        token = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(token.access_token),
                # "user": {
                #     "email": user.email,
                #     "first_name": user.first_name,
                #     "last_name": user.last_name,
                # },
            },
            status=status.HTTP_200_OK,
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
    description="Retrieve a list of all health advisors",
    tags=["Users"],
    responses={
        200: OpenApiResponse(
            response=RetrieveUserSerializer,
            description="List of health advisors retrieved successfully",
        ),
        400: OpenApiResponse(description="Invalid request"),
    },
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
