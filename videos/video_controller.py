from .models import Video, Tagging


def get_all_taggings_for_video(video_id):
    return Tagging.objects.filter(related_video=video_id)
