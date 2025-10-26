from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    title = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    otpCode = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title