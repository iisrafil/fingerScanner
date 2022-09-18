from django.db import models


class Registered(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    finger = models.ImageField(upload_to="Registered")
