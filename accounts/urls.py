from django.urls import path

from .views import UserCreateAPIView

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="create-user"),
]
