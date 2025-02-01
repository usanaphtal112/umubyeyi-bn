from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .models import LastMenstrualPeriod
from .serializers import LastMenstrualPeriodSerializer, DashboardSerializer


@extend_schema(
    description="Create or update last menstrual period information for a user",
    tags=["Umubyeyi"],
    request=LastMenstrualPeriodSerializer,
    responses={
        201: OpenApiResponse(
            response=LastMenstrualPeriodSerializer,
            description="Last menstrual period information created successfully",
        ),
        400: OpenApiResponse(
            description="Invalid input data",
            examples=[
                OpenApiExample(
                    "Validation Error", value={"date": ["This field is required."]}
                )
            ],
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided"
        ),
    },
    examples=[
        OpenApiExample(
            "Valid Request",
            value={"date": "2024-03-15", "cycle_length": 28},
            request_only=True,
        )
    ],
)
class LastMenstrualPeriodAPIView(APIView):
    serializer_class = LastMenstrualPeriodSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise AuthenticationFailed("Authentication credentials were not provided.")
        serializer = LastMenstrualPeriodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Retrieve pregnancy-related dashboard information for the authenticated user",
    tags=["Umubyeyi"],
    responses={
        200: OpenApiResponse(
            response=DashboardSerializer,
            description="Dashboard data retrieved successfully",
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided"
        ),
    },
)
class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        lmp_instances = LastMenstrualPeriod.objects.filter(user=request.user)
        for instance in lmp_instances:
            instance.update_pregnancy_info()
            # instance.save()
        serializer = DashboardSerializer(lmp_instances, many=True)
        return Response(serializer.data)
