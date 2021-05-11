from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Myuser(AbstractUser):
    medium=models.CharField(default="medium", max_length=100)

class Document(models.Model):
    docfile = models.FileField(upload_to='')

class MyDevice(models.Model):
    mainPort = models.IntegerField()
    subPort = models.IntegerField()
    deviceName = models.CharField(max_length=16)
    deviceSpeed = models.CharField(max_length=16)
    deviceBus = models.IntegerField()
    
