from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Tweet(models.Model):
  time = models.DateTimeField(auto_now=True)
  author = models.CharField(max_length=40)
  content = models.CharField(max_length=280)
  likes = models.ManyToManyField(User)

  def __str__(self):
    return self.content

  def __len__(self):
    return len(self.content)

class Hashtag(models.Model):
  tweets = models.ManyToManyField(Tweet)
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

class Replies(models.Model):
  content = models.CharField(max_length=280)
  tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
  author = models.CharField(max_length=40)
  time = models.DateTimeField(auto_now=True)
