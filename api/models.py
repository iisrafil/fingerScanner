from django.db import models
from django.utils import timezone

from scanner.models import Finger


class Device(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    location = models.TextField()


class Intruder(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    finger = models.ForeignKey(Finger, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Intruders')


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    finger = models.ForeignKey(Finger, on_delete=models.CASCADE)
    match_result = models.BooleanField(blank=True, Null=True)
    match_time = models.FloatField(blank=True, Null=True)
    match_percent = models.FloatField(blank=True, Null=True)
    transport_time = models.FloatField(blank=True, Null=True)
    transport_medium = models.CharField(blank=True, Null=True)
    photo = models.ForeignKey(Intruder, on_delete=models.CASCADE)
    photo_time = models.FloatField(blank=True, Null=True)
