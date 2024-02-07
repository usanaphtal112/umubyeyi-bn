from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.utils import extend_schema
from .models import LastMenstrualPeriod
from .serializers import LastMenstrualPeriodSerializer, DashboardSerializer


@extend_schema(
    description="Last Menstrual period endpoint",
    tags=["Umubyeyi"],
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
    description="Umubyeyi dashboard",
    tags=["Umubyeyi"],
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
