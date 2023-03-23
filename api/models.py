from django.db import models


class Device(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    location = models.TextField()
    depth = models.IntegerField(default=100)


class Finger(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(upload_to='finger_scan')


class Intruder(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    finger = models.ForeignKey(Finger, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Intruders')


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    finger = models.OneToOneField(Finger, on_delete=models.CASCADE)
    match_result = models.BooleanField(blank=True, null=True)
    match_time = models.FloatField(blank=True, null=True)
    match_percent = models.FloatField(blank=True, null=True)
    transport_time = models.FloatField(blank=True, null=True)
    transport_medium = models.CharField(max_length=30, blank=True, null=True)
    photo = models.OneToOneField(Intruder, on_delete=models.CASCADE)
    photo_time = models.FloatField(blank=True, null=True)