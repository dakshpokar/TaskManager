from django.db import models
from django.contrib.auth.models import User


def user_directory(instance, filename):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	return str(instance.username) + "/" + "profile_picture"

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=400)
    profile_picture = models.FileField(upload_to=user_directory, null=True, default='/default_profile.jpg', blank=True)

class Teams(models.Model):    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='Membership', related_name="member")

class Task(models.Model):
    id = models.AutoField(primary_key=True)

class Membership(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)