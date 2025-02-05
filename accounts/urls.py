from django.urls import path

from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    HealthAdvisorListView,
    UserListAPIView,
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="create-user"),
    path("auth/login/", LoginAPIView.as_view(), name="user-login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="user-logout"),
    path(
        "users/health-advisor/",
        HealthAdvisorListView.as_view(),
        name="health-advisor-list",
    ),
    path("users/", UserListAPIView.as_view(), name="user-list"),
]
