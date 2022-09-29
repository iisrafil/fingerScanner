from django.db import models
from django.contrib.auth.models import AbstractUser;

# Create your models here.

class Account(AbstractUser):
    address = models.TextField(max_length=200, default="5B/13, Razia Sultana Road, Mohammadpur, Dhaka-1207, Bangladesh.");
    phone = models.CharField(max_length=20, default="01923240000");
    
    approved = models.BooleanField(default=False);

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
    phone = models.CharField(max_length=20, default="01923240000");
    address = models.TextField(max_length=200, default="5B/13, Razia Sultana Road, Mohammadpur, Dhaka-1207, Bangladesh.");
    approved = models.BooleanField(default=False);

    def __str__(self) -> str:
        return self.name;

class Fingerprint(models.Model):
    of = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False);

    finger = models.CharField(choices=(
        ("ri", "right_index"), ("rm", "right_middle"), ("rr", "right_ring"), ("rl", "right_little"), ("rt", "right_thumb"), ("li", "left_index"), ("lm", "left_middle"), ("lr", "left_ring"), ("ll", "left_little"), ("lt", "left_thumb"),
    ), max_length=20);
    img = models.ImageField(upload_to="prints");

    def __str__(self) -> str:
        return str(self.of)+":"+self.finger;
