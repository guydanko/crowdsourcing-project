from __future__ import absolute_import, unicode_literals
from celery import shared_task
from videos.transcript_score import get_transcript_score
from .models import Tagging, User, Video
from celery.utils.log import get_task_logger
from Project.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True)
def update_transcript_score_async(self, json_transcript, description, start_seconds, end_seconds, tag_id):
    try:
        transcript_score = get_transcript_score(json_transcript, start_seconds, end_seconds, description)
    except Exception:
        # just in case
        transcript_score = 0
    try:
        tag = Tagging.objects.get(id=tag_id)
        tag.transcript_score = transcript_score
        tag.save()
    except Tagging.DoesNotExist:
        print("tag was deleted while transcript score was calculated")