from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to='images/users/', blank=True, null=True)
    phone_no = models.CharField(max_length=11, null=True, blank=True)
    is_special = models.BooleanField(default=False, blank=True)
    about_me = models.TextField(null=True, blank=True)

class Verification(models.Model):
    email = models.EmailField(primary_key=True)
    username =  models.CharField(max_length=255)
    token = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    token = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
