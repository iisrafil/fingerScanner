from django.db import models
from django.contrib.auth.models import AbstractUser;

# Create your models here.

class Account(AbstractUser):
    address = models.TextField(max_length=200, default="No Address");

class Vehicle(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=False);

    license_no = models.CharField(max_length=50, unique=True);
    last_location = models.CharField(max_length=100, null=True);
    approved = models.BooleanField(default=False);

    def __str__(self) -> str:
        return str(self.id) + ":" + str(self.owner.username);

class Driver(models.Model):
    vehicles = models.ManyToManyField(Vehicle);

    name = models.CharField(max_length=20);
    license_no = models.CharField(max_length=50, unique=True, null=False);
    address = models.TextField(max_length=200, default="No Address");
    approved = models.BooleanField(default=False);
    
    def __str__(self) -> str:
        return self.name;