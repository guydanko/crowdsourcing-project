import json
import youtube_transcript_api
from django.db import models
from django.contrib.postgres.fields import JSONField
from embed_video.fields import EmbedVideoField
from datetime import datetime as dt
import datetime
from django.contrib.auth.models import User
from youtube_transcript_api import YouTubeTranscriptApi as yt
import youtube_dl

sID = "t99ULJjCsaM"

date = datetime.date(1, 1, 1)
MAX_START_TO_END_RANGE = dt.combine(date, datetime.time(0, 5, 0)) - \
                         dt.combine(date, datetime.time(0, 0, 0))


def seconds_to_time(duration_in_seconds):
    hours = duration_in_seconds // 3600
    minutes = (duration_in_seconds % 3600) // 60
    seconds = duration_in_seconds % 60
    return datetime.time(hours, minutes, seconds)


class Video(models.Model):
    video = EmbedVideoField()  # it's just the video url
    duration = models.TimeField(verbose_name="Duration(hh:mm:ss):")
    transcript = JSONField(blank=True, default="Leave empty")

    def save(self, *args, **kwargs):
        # checks if video has transcript
        try:
            duration_in_seconds = youtube_dl.YoutubeDL().extract_info(self.video.format(sID=sID))['duration']
            self.duration = seconds_to_time(duration_in_seconds)
            self.transcript = json.dumps(yt.get_transcript(self.video.split('=')[1]))
        except youtube_transcript_api.TranscriptsDisabled:
            raise Exception(f"{self.video} doesn't have transcript continue")
        # checks if the video is already in the db
        for vid in Video.objects.all():
            if vid.video == self.video:
                return
        super().save(*args, **kwargs)


class TaggingValidator:
    @classmethod
    def get_errors(cls, creator, video, start, end, date_subscribed, description, rating_value):
        errors = []
        time_range = dt.combine(date, start) - dt.combine(date, end)
        if dt.combine(date, start) < dt.combine(date, dt.time(0, 0, 0)) or \
                dt.combine(date, end) > dt.combine(date, video.length):
            errors.append(f'Time out of range')
        if time_range > MAX_START_TO_END_RANGE:
            errors.append(f'Invalid time range, Maximal valid time range duration is {MAX_START_TO_END_RANGE}')
        return errors


class Tagging(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    start = models.TimeField(verbose_name="Start(hh:mm:ss):")
    end = models.TimeField(verbose_name="End(hh:mm:ss):")
    date_subscribed = models.DateTimeField(default=dt.now())
    description = models.TextField(verbose_name="Subject description:", max_length=50)
    rating_value = models.IntegerField(default=0)


class UserRating(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tagging = models.ForeignKey(Tagging, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
