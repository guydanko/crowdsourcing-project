from __future__ import absolute_import, unicode_literals
from celery import shared_task
from videos.transcript_score import get_transcript_score
from .models import Tagging, User, Video
from celery.utils.log import get_task_logger
from Project.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True)
def get_transcript_score_async(self, json_transcript, user_id, start_time, end_time, description, video_id, start_seconds, end_seconds):
    try:
        transcript_score = get_transcript_score(json_transcript, start_seconds, end_seconds, description)
    except Exception:
        transcript_score = 0
    user = User.objects.get(id=user_id)
    video = Video.objects.get(id=video_id)
    tag = Tagging.objects.create(creator=user, start=start_time, start_seconds=start_seconds, end=end_time, end_seconds=end_seconds,
                                 description=description, video=video, transcript_score=transcript_score)
    tag.save()
    return transcript_score