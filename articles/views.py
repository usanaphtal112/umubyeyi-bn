from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAdminOrHealthAdvisorOrReadOnly
from drf_spectacular.utils import extend_schema


@extend_schema(
    description="View the articles",
    tags=["Articles"],
)
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrHealthAdvisorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(
    description="View the articles",
    tags=["Articles"],
)
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrHealthAdvisorOrReadOnly]

    lookup_field = "slug"

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        slug = self.kwargs.get(self.lookup_field)
        obj = generics.get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj
