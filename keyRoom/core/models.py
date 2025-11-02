from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    uniquiCode = models.CharField(max_length=100, unique=True)

class CustomTag(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='custom_tags')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Credential(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='credentials')
    tag = models.ForeignKey(CustomTag, on_delete=models.SET_NULL, related_name='credentials', null=True,  blank=True)
    title = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    otpCode = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

class ListOfTrustedUsers(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='trusted_list')
    trusted_users = models.ManyToManyField(CustomUser, related_name='trusted_in_list', blank=True)

    def __str__(self):
        return f"{self.owner.username}'s trusted users list"