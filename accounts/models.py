from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Avatar stored as raw bytes in the database — no filesystem dependency
    avatar_data = models.BinaryField(null=True, blank=True)
    avatar_content_type = models.CharField(max_length=50, blank=True, default='')
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def has_avatar(self):
        return self.avatar_data is not None and len(self.avatar_data) > 0

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
