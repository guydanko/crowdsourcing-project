import json
from django.db import models
from django.contrib.postgres.fields import JSONField
from embed_video.fields import EmbedVideoField
from datetime import datetime
from django.contrib.auth.models import User
from youtube_transcript_api import YouTubeTranscriptApi as yt


class Video(models.Model):
    video = EmbedVideoField()  # it's just the video url
    transcript = JSONField(blank=True)

    def save(self, *args, **kwargs):
        # saves the transcript as a json object in the db
        # TODO need to test case if the video doesn't have any transcript then shouldn't be added to the site
        self.transcript = json.dumps(yt.get_transcript(self.video.split('=')[1]))
        super().save(*args, **kwargs)


class Tagging(models.Model):
    start = models.DurationField()
    end = models.DurationField()
    date_subscribed = models.DateTimeField(default=datetime.now())
    description = models.TextField(max_length=200)
    related_video = models.CharField(max_length=200, default="empty")
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, default=00)
