from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView, PostListView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<slug:slug>/update/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
]
