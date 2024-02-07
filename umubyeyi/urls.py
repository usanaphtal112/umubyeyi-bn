from django.urls import path
from .views import LastMenstrualPeriodAPIView, DashboardAPIView

urlpatterns = [
    path(
        "last-menstrual-period/",
        LastMenstrualPeriodAPIView.as_view(),
        name="last-menstrual-period",
    ),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]
