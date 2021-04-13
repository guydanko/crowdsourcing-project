from django.db import models
from django.forms import ModelForm
from embed_video.fields import EmbedVideoField
import datetime
from django.contrib.auth.models import User

date = datetime.date(1, 1, 1)
MAX_START_TO_END_RANGE = datetime.datetime.combine(date, datetime.time(0, 5, 0)) - \
                         datetime.datetime.combine(date, datetime.time(0, 0, 0))


class Video(models.Model):
    video = EmbedVideoField()  # same like models.URLField()
    length = models.TimeField()


class UserRating(models.Model):
    creator = models.ForeignKey(User, related_name='creator_user_rating', on_delete=models.CASCADE)
    tagging = models.ForeignKey(User, related_name='tagging_user_rating', on_delete=models.CASCADE)
    is_upvote = models.BooleanField()


class TaggingValidator:
    @classmethod
    def get_errors(cls, creator, video, start, end, date_subscribed, description, rating_value):
        errors = []
        time_range = datetime.datetime.combine(date, start) - datetime.datetime.combine(date, end)
        if datetime.datetime.combine(date, start) < datetime.datetime.combine(date, datetime.time(0, 0, 0)) or \
                datetime.datetime.combine(date, end) > datetime.datetime.combine(date, video.length):
            errors.append(f'Time out of range')
        if time_range > MAX_START_TO_END_RANGE:
            errors.append(f'Invalid time range, Maximal valid time range duration is {MAX_START_TO_END_RANGE}')


class Tagging(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()
    date_subscribed = models.DateTimeField(default=datetime.datetime.now())
    description = models.TextField(max_length=50)
    rating_value = models.IntegerField(default=0)
