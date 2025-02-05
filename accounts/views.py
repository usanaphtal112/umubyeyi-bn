from django.contrib.auth import authenticate, get_user_model
from django.db import transaction, models
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlacklistedToken
from .serializers import (
    CustomUserSerializer,
    UserLoginSerializers,
    RetrieveUserSerializer,
)
from .validations import (
    is_phonenumber_already_registered,
)
from datetime import timedelta

User = get_user_model()


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
            # Attempt to authenticate the user.
            user = authenticate(
                request=request,
                phone_number=serializer.validated_data["phone_number"],
                password=serializer.validated_data["password"],
            )
            # If authentication fails, raise a ValidationError.
            if user is None:
                raise serializers.ValidationError("Invalid credentials.")
        except serializers.ValidationError:
            # Return error response with the desired message format.
            return Response(
                {"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

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


class LogoutAPIView(APIView):
    """
    API endpoint for user logout.
    Blacklists the access token to prevent further use.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Logout user by blacklisting the access token",
        tags=["Authentication"],
        responses={
            200: OpenApiResponse(
                description="Logout successful",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={"message": "Successfully logged out"},
                    )
                ],
            ),
            401: OpenApiResponse(
                description="Unauthorized",
                examples=[
                    OpenApiExample(
                        "Error Response",
                        value={"error": "No valid token found"},
                    )
                ],
            ),
        },
    )
    def post(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"error": "No valid token found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        with transaction.atomic():
            BlacklistedToken.objects.create(token=token, blacklisted_at=now())

            # Delete tokens older than 3 months
            expiry_date = now() - timedelta(days=90)
            BlacklistedToken.objects.filter(blacklisted_at__lt=expiry_date).delete()

        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )


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
    permission_classes = [IsAuthenticated]

    serializer_class = RetrieveUserSerializer

    def get_queryset(self):
        role_name = User.Role.HEALTH_ADVISOR
        queryset = RetrieveUserSerializer.filter_by_role(role_name)
        return queryset

    def handle_exception(self, exc):
        if isinstance(exc, serializers.ValidationError):
            # Return the custom error response
            return Response({"detail": exc.detail}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


@extend_schema(
    description="Retrieve a list of all users excluding Health Advisor, and Health center",
    tags=["Users"],
    responses={
        200: OpenApiResponse(
            response=RetrieveUserSerializer,
            description="List of users excluding Health Advisor, and Health center retrieved successfully",
        ),
        400: OpenApiResponse(description="Invalid request"),
    },
)
class UserListAPIView(generics.ListAPIView):
    """
    API endpoint for user.
    Lists out all Users Excluding user with ADMIN, HEALTH ADVISOR AND HEALTH CENTER role users.
    """

    permission_classes = [IsAuthenticated]

    serializer_class = RetrieveUserSerializer
    queryset = User.objects.all().exclude(
        models.Q(role=User.Role.ADMIN)
        | models.Q(role=User.Role.HEALTH_ADVISOR)
        | models.Q(role=User.Role.HEALTH_CENTER)
    )
