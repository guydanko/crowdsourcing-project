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
# MAX_START_TO_END_RANGE = dt.combine(date, datetime.time(0, 5, 0)) - \
#                          dt.combine(date, datetime.time(0, 0, 0))

MAX_START_TO_END_RANGE = 5 * 60
MIN_START_TO_END_RANGE = 5

def seconds_to_time(duration_in_seconds):
    hours = duration_in_seconds // 3600
    minutes = (duration_in_seconds % 3600) // 60
    seconds = duration_in_seconds % 60
    return datetime.time(hours, minutes, seconds)


def time_to_seconds(time_object):
    return time_object.hour * 3600 + time_object.minute * 60 + time_object.second


class Video(models.Model):
    video = EmbedVideoField()
    duration = models.TimeField(verbose_name="Duration(hh:mm:ss):")
    transcript = JSONField(blank=True, default="Leave empty")
    name = models.CharField(blank=True, max_length=500)

    def save(self, *args, **kwargs):
        # checks if video has transcript
        try:
            # yt api gets the suffix of the video url after the =
            self.transcript = json.dumps(yt.get_transcript(self.video.split('=')[1]))
        except youtube_transcript_api.TranscriptsDisabled:
            raise Exception(f"{self.video} doesn't have transcript continue")
        # checks if the video is already in the db
        for vid in Video.objects.all():
            if vid.video == self.video:
                return
        # if validation passed - save duration and name
        video_info = youtube_dl.YoutubeDL().extract_info(self.video.format(sID=sID), download=False)
        self.duration = seconds_to_time(video_info['duration'])
        self.name = video_info['title']

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TaggingValidator:
    @classmethod
    def get_errors(cls, creator, video, start, end, description, date_subscribed=None, rating_value=None):
        errors = []
        start = dt.combine(date, start)
        end = dt.combine(date, end)
        start_in_seconds = time_to_seconds(start)
        end_in_seconds = time_to_seconds(end)
        time_range_in_seconds = end_in_seconds - start_in_seconds
        video_length_in_seconds = time_to_seconds(dt.combine(date, video.duration))
        if start_in_seconds < 0 or end_in_seconds > video_length_in_seconds:
            errors.append(f'Time out of range')
        if time_range_in_seconds > MAX_START_TO_END_RANGE:
            errors.append(f'Invalid time range, Maximal valid time range duration is {MAX_START_TO_END_RANGE}')
        if time_range_in_seconds < MIN_START_TO_END_RANGE:
            errors.append(f'Invalid time range, Minimal valid time range duration is {MIN_START_TO_END_RANGE}')
        return errors


class Tagging(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    start = models.TimeField(verbose_name="Start(hh:mm:ss):")
    end = models.TimeField(verbose_name="End(hh:mm:ss):")
    date_subscribed = models.DateTimeField(default=dt.now())
    description = models.TextField(verbose_name="Subject description:", max_length=50)
    rating_value = models.IntegerField(default=0)


class UserRatingValidator:
    @classmethod
    def get_errors(cls, creator, tagging, is_upvote):
        errors = []
        if not tagging.exists():
            errors.append("Tag doesn't exist")
            return errors
        if tagging.creator == creator:
            errors.append("Creator matches rater")
            return errors


class UserRating(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tagging = models.ForeignKey(Tagging, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
