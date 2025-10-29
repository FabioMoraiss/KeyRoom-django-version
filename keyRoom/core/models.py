from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_tags')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    tag = models.ForeignKey(CustomTag, on_delete=models.SET_NULL, related_name='credentials', null=True,  blank=True)
    title = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    otpCode = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

class SharedCredential(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE, related_name='shared_with')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_credentials')
    shared_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_credentials')