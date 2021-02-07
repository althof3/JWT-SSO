from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    npm = models.CharField(max_length=10)
    email = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=50, null=True)
    org_code = models.CharField(max_length=20, null=True)
    data = models.TextField(default="{}")

    def __str__(self):
        return self.name