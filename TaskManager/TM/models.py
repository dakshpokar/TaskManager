from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teams(models.Model):    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    members = models.ManyToManyField(User)

class Task(models.Model):
    id = models.AutoField(primary_key=True)

