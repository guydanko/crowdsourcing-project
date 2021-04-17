import json

import youtube_transcript_api
from django.db import models
from django.contrib.postgres.fields import JSONField
from embed_video.fields import EmbedVideoField
from datetime import datetime
from django.contrib.auth.models import User
from youtube_transcript_api import YouTubeTranscriptApi as yt


class Video(models.Model):
    video = EmbedVideoField()  # it's just the video url
    transcript = JSONField(blank=True, default="Leave empty")

    def save(self, *args, **kwargs):
        # checks if video has transcript
        try:
            self.transcript = json.dumps(yt.get_transcript(self.video.split('=')[1]))
        except youtube_transcript_api.TranscriptsDisabled:
            raise Exception(f"{self.video} doesn't have transcript continue")
        # checks if the video is already existed in the db
        for vid in Video.objects.all():
            if vid.video == self.video:
                return
        super().save(*args, **kwargs)


class Tagging(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    start = models.TimeField(verbose_name="Start(hh:mm:ss):")
    end = models.TimeField(verbose_name="End(hh:mm:ss):")
    date_subscribed = models.DateTimeField(default=datetime.now())
    description = models.TextField(verbose_name="Subject description:", max_length=50)
    rating_value = models.IntegerField(default=0)


class UserRating(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tagging = models.ForeignKey(Tagging, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
