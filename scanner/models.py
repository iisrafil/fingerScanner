from django.db import models

from api.models import Device


class FingerScn(models.Model):
    device = models.ForeignKey(Device, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(upload_to='finger_scan')


class Registered(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    finger = models.ImageField(upload_to="Registered")
