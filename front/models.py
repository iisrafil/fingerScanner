from django.db import models
from django.contrib.auth.models import AbstractUser;

# Create your models here.

class Account(AbstractUser):
    address = models.CharField(max_length=100);