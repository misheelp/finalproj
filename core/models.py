from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Tweet(models.Model):
  time = models.DateTimeField(auto_now=True)
  author = models.CharField(max_length=40)
  content = models.CharField(max_length=280)
  likes = models.ManyToManyField(User)

class Hashtag(models.Model):
  tweets = models.ManyToManyField(Tweet)
  name = models.CharField(max_length=50)