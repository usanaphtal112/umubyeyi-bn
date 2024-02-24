from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="article_posts"
    )
    body = models.TextField()
    published_on = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ["-published_on"]
        indexes = [
            models.Index(fields=["-published_on"]),
        ]

    def __str__(self):
        return self.title
