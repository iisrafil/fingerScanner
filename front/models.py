from django.db import models
from django.contrib.auth.models import AbstractUser;

# Create your models here.

class Account(AbstractUser):
    address = models.TextField(max_length=200, default="No Address");

class Vehicle(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=False);

    license_no = models.CharField(max_length=50, unique=True);
    last_location = models.CharField(max_length=100, null=True);