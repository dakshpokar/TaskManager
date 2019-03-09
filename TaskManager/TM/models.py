from django.db import models
from django.contrib.auth.models import User
import time

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
    url = models.CharField(max_length=400)
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, through='Membership', related_name="member")

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    belongs_to = models.ForeignKey(Teams, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    desc = models.TextField()
    assigned_members = models.ManyToManyField(UserProfile, through='MembershipToTask', related_name="memberOfTask")
    status = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=400)


class MembershipToTask(models.Model):
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

class Membership(models.Model):
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    date_generated = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    