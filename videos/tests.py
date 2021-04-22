import datetime
from django.test import TestCase
from videos.video_controller import get_all_videos, get_user_rating_for_tagging, get_all_ratings_for_tagging, get_all_taggings_for_video, create_user_rating, create_tagging
from videos.models import Video, Tagging, UserRating
from django.contrib.auth.models import User


# Create your tests here.
class ManualTest(TestCase):
    def test_functionality(self):
        Video.objects.create(video='https://www.youtube.com/watch?v=NC45TRP4lq0&ab_channel=Vox')
        Video.objects.create(video='https://www.youtube.com/watch?v=0MrgsYswT1c&ab_channel=TheDumbfounds')
        user1 = User.objects.create(username='Mark', password='Zuckerberg')
        user2 = User.objects.create(username="Guy", password='Danko')
        videos = get_all_videos()
        video1 = videos[0]
        video2 = videos[1]
        Tagging.objects.create(creator=user1, video=video1, start=datetime.time(0, 5, 45), end=datetime.time(0, 6, 45), description='hello')
        tagging1 = get_all_taggings_for_video(video1)[0]
        create_user_rating(user1, tagging1, True)
        print(tagging1.rating_value)
        create_user_rating(user1, tagging1, False)
        print(tagging1.rating_value)
        print("done")


