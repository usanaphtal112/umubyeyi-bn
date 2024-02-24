from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "body", "published_on", "status"]
        read_only_fields = ["id", "published_on"]

    def create(self, validated_data):
        validated_data["slug"] = self.generate_slug(validated_data["title"])
        return super().create(validated_data)

    def generate_slug(self, title):
        return title.lower().replace(" ", "-")
