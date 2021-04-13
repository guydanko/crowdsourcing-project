import datetime
from django.test import TestCase
from videos.video_controller import get_all_videos, get_user_rating_for_tagging, get_all_ratings_for_tagging, get_all_taggings_for_video, create_user_rating, create_tagging
from videos.models import Video, Tagging, UserRating
from django.contrib.auth.models import User


# Create your tests here.
class ManualTest(TestCase):
    def test_functionality(self):
        Video.objects.create(video='https://www.youtube.com/watch?v=NC45TRP4lq0&ab_channel=Vox',
                             length=datetime.time(0, 33, 45))
        Video.objects.create(video='https://www.youtube.com/watch?v=0MrgsYswT1c&ab_channel=TheDumbfounds',
                             length=datetime.time(0, 55, 45))
        user1 = User.objects.create(username='Mark', password='Zuckerberg')
        user2 = User.objects.create(username="Guy", password='Danko')
        videos = get_all_videos()
        video1 = videos[0]
        video2 = videos[1]
