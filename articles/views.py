from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied
from umubyeyi.models import LastMenstrualPeriod
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="View the articles",
    tags=["Articles"],
)
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            lmp = LastMenstrualPeriod.objects.filter(user=user).first()
            if lmp:
                trimester = lmp.trimester
                queryset = Post.published.filter(trimester=trimester)
                return queryset
            else:
                return Post.published.none()
        else:
            raise PermissionDenied("You must be logged in to view articles.")


@extend_schema(
    description="Create Article posts",
    tags=["Articles"],
)
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            raise PermissionDenied("You must be logged in to create a post.")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Article created successfully."}, status=status.HTTP_201_CREATED
        )


@extend_schema(
    description="Update or edit Article posts",
    tags=["Articles"],
)
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@extend_schema(
    description="Delete Article posts",
    tags=["Articles"],
)
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
