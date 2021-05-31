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
from .Utils import *

sID = "t99ULJjCsaM"

date = datetime.date(1, 1, 1)
# MAX_START_TO_END_RANGE = dt.combine(date, datetime.time(0, 5, 0)) - \
#                          dt.combine(date, datetime.time(0, 0, 0))

MAX_START_TO_END_RANGE = 20 * 60
MIN_START_TO_END_RANGE = 5
TAG_VALIDATION_THRESHOLD = 0.2


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
    length_in_sec = models.IntegerField(blank=True)
    bucket_size = models.IntegerField(blank=True)

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

        video_info = youtube_dl.YoutubeDL().extract_info(self.video.format(sID=sID), download=False)
        self.duration = seconds_to_time(video_info['duration'])
        self.name = video_info['title']
        self.length_in_sec = video_info['duration']
        self.bucket_size = compute_video_bucket_length(self.length_in_sec)

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
    # General Info - Not subjective to Change after creation
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # start = models.TimeField(verbose_name="Start(hh:mm:ss):")
    start = models.TimeField(verbose_name="Start:")
    start_seconds = models.DecimalField(decimal_places=2, max_digits=10)
    # end = models.TimeField(verbose_name="End(hh:mm:ss):")
    end = models.TimeField(verbose_name="End:")
    end_seconds = models.DecimalField(decimal_places=2, max_digits=10)
    date_subscribed = models.DateTimeField(default=dt.now())
    description = models.TextField(verbose_name="Subject description:", max_length=50)
    transcript_score = models.FloatField()

    # like/dislike counters, and scores that are dynamically changed each save
    rating_value = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    rating_score = models.FloatField(default=0)  # aggregated score using wilson's CI lowerbound
    total_tag_score = models.FloatField(default=0)
    is_validated = models.BooleanField(default=False)  # purpose to prioritize from 'non validated' tags

    is_invalid = models.BooleanField(default=False)  # purpose to put in 'trash'

    def __str__(self):
        return f"Tagging description - {self.description}"

    def save(self, *args, **kwargs):
        self.rating_score = rating_score_calc(self.up_votes, self.down_votes)
        self.total_tag_score = calculate_total_rating_score_for_tag(self.rating_score, self.transcript_score)
        if is_tag_invalid(self.up_votes, self.down_votes):
            self.is_invalid = True
        elif self.total_tag_score >= TAG_VALIDATION_THRESHOLD:
            self.is_validated = True
        else:
            self.is_validated = False
        super().save(*args, **kwargs)


class UserRatingValidator:
    @classmethod
    def get_errors(cls, creator, tagging, is_upvote):
        errors = []
        if not tagging:
            errors.append("Tag doesn't exist")
            return errors
        if tagging.creator == creator:
            errors.append("Creator matches rater")
            return errors


class UserRating(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tagging = models.ForeignKey(Tagging, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tagging, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creator_name = models.TextField(max_length=150, default="")
    body = models.TextField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    is_reply = models.BooleanField(default=False)

    class Meta:
        ordering = ('creation_date',)

    def __str__(self):
        return f'Comment by {self.creator}, content - {self.body}'
