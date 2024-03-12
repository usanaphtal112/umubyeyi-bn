from django.urls import path

from .views import (
    CreateUserRoleAPIView,
    UserCreateAPIView,
    UserLoginAPIView,
    HealthAdvisorListView,
)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="create-user"),
    path("role/", CreateUserRoleAPIView.as_view(), name="create-role"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path(
        "health-advisor/", HealthAdvisorListView.as_view(), name="health-advisor-list"
    ),
]
