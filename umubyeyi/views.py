from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import LastMenstrualPeriod
from .serializers import LastMenstrualPeriodSerializer, DashboardSerializer


@extend_schema(
    description="Last Menstrual period endpoint",
    tags=["Umubyeyi"],
)
class LastMenstrualPeriodAPIView(APIView):
    serializer_class = LastMenstrualPeriodSerializer

    def post(self, request, format=None):
        serializer = LastMenstrualPeriodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Umubyeyi dashboard",
    tags=["Umubyeyi"],
)
class DashboardAPIView(APIView):
    def get(self, request, format=None):
        lmp_instances = LastMenstrualPeriod.objects.all()
        for instance in lmp_instances:
            instance.update_pregnancy_info()
            # instance.save()
        serializer = DashboardSerializer(lmp_instances, many=True)
        return Response(serializer.data)
