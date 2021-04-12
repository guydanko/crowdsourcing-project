from django.db import models
from django.forms import ModelForm
from embed_video.fields import EmbedVideoField
from datetime import datetime

class Video(models.Model):
    video = EmbedVideoField()  # same like models.URLField()



class Tagging(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    date_subscribed = models.DateTimeField(default=datetime.now())
    description = models.TextField(max_length=200)
