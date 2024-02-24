from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "published_on", "status"]
    list_filter = ["status", "created_at", "published_on", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "published_on"
    ordering = ["status", "published_on"]
