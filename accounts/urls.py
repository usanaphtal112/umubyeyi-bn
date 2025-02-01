from django.urls import path

from .views import (
    RegisterAPIView,
    CreateUserRoleAPIView,
    LoginAPIView,
    HealthAdvisorListView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="create-user"),
    path("role/", CreateUserRoleAPIView.as_view(), name="create-role"),
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path(
        "health-advisor/", HealthAdvisorListView.as_view(), name="health-advisor-list"
    ),
]
