# import datetime
from django.test import TestCase
# from videos.video_controller import get_all_videos, get_all_tags_for_video, create_user_rating, create_tagging
# from videos.models import Video, Tagging, UserRating
# from django.contrib.auth.models import User
import json
from videos.transcript_score import get_transcript_score


# Create your tests here.
class ManualTest(TestCase):
    def test_functionality(self):
        # Video.objects.create(video='https://www.youtube.com/watch?v=NC45TRP4lq0&ab_channel=Vox')
        # Video.objects.create(video='https://www.youtube.com/watch?v=0MrgsYswT1c&ab_channel=TheDumbfounds')
        # user1 = User.objects.create(username='Mark', password='Zuckerberg')
        # user2 = User.objects.create(username="Guy", password='Danko')
        # videos = get_all_videos()
        # video1 = videos[0]
        # video2 = videos[1]
        # Tagging.objects.create(creator=user1, video=video1, start=datetime.time(0, 5, 45), end=datetime.time(0, 5, 45), description='hello')
        # print(create_tagging(video1, user1, datetime.time(0, 5, 45), datetime.time(0, 5, 45), 'hello'))
        # all_tags = get_all_tags_for_video(video1)
        # print(all_tags)
        # tagging1 = all_tags[0]
        # print(tagging1)
        # print(create_user_rating(user2, tagging1, True))
        # print(tagging1.rating_value)
        # print(create_user_rating(user2, tagging1, False))
        # print(tagging1.rating_value)
        # print("done")
        pass


    def test_transcript_score_functionality(self):
        users_tag_text = "something about / [ ] a nuclear war and democracies and something"
        transcript = [{"text": "So if you read the headlines, it kind of seems\nlike the world is a terrible place, full of",
          "start": 1.449, "duration": 4.401},
         {"text": "violence, despair, and war. But it turns out\nwar is actually declining. We live in the",
          "start": 5.85, "duration": 4.72},
         {"text": "most peaceful time in human history. There's\nlots of reasons why, but here are three of",
          "start": 10.57, "duration": 4.58},
         {"text": "the biggest ones. First, the spread of democracy\naround the world. International relations",
          "start": 15.15, "duration": 4.71},
         {"text": "scholars have found consistently that democracies\ndon't fight wars with each other. Now why",
          "start": 19.86, "duration": 4.62},
         {"text": "is that true? There might be plenty of reasons\nbut one big one is that people who live in",
          "start": 24.48, "duration": 4.64},
         {"text": "democracies think it's wrong to start wars\nwith other democracies. They're legitimate",
          "start": 29.12, "duration": 4.2},
         {"text": "governments -- it's wrong to attack them.\nBut there's a flipside to this. Democracies",
          "start": 33.32, "duration": 4.56},
         {"text": "do often fight wars with autocracies. Luckily,\nmost of the world's countries are democracies now,",
          "start": 37.88, "duration": 4.77},
         {"text": "so the democratic peace is probably making\nthe world a much more peaceful place. Second",
          "start": 42.65, "duration": 5.01},
         {"text": "big reason why war is declining is nuclear\ndeterrence. Nuclear weapons, obviously big",
          "start": 47.66, "duration": 4.6},
         {"text": "and scary. However, nuclear deterrence may\nhave prevented a devastating war between the",
          "start": 52.26, "duration": 4.819},
         {"text": "United States and the Soviet Union. Everyone\nrecognized that they would lose. Statistical",
          "start": 57.079, "duration": 4.261},
         {"text": "evidence suggests that that is true -- that\nmost countries are too scared of the consequences",
          "start": 61.34, "duration": 4.669},
         {"text": "of nuclear war to fight one. There's a dark\nside, and not just the risk of global annihilation",
          "start": 66.009, "duration": 4.5},
         {"text": "from an accident. If a country gets nuclear\nweapons, they feel rather safer in being aggressive",
          "start": 70.509, "duration": 6.63},
         {"text": "in little ways, you know, small conflicts\nor bullying around their non-nuclear neighbors.",
          "start": 77.139, "duration": 5.26},
         {"text": "This weird paradox, that nuclear weapons make\nthe world more violent and more peaceful at",
          "start": 82.399, "duration": 4.72},
         {"text": "the same time, is called the Stability-Instability\nParadox. The third reason that war has declined",
          "start": 87.119, "duration": 5.27},
         {"text": "has been the spread of the idea of national\nsovereignty. This idea is hundreds of years",
          "start": 92.389, "duration": 3.951},
         {"text": "old, the idea that you shouldn't interfere\ninside the borders of another state. But people",
          "start": 96.34, "duration": 4.619},
         {"text": "didn't take the idea too seriously, because\nstealing new land used to be a major cause of",
          "start": 100.959, "duration": 3.77},
         {"text": "war. Think American European colonialism or\nWorld War II. But after World War II, nations",
          "start": 104.729, "duration": 4.75},
         {"text": "pledged to stop. Since 1976 there hasn't been\na single successful war of conquest, except",
          "start": 109.479, "duration": 5.361},
         {"text": "for maybe Russia in Crimea, really recently.\nAgain though, sovereignty has a flip side.",
          "start": 114.84, "duration": 4.949},
         {"text": "Sometimes governments go to war against their\nown people, and poor, weak governments often",
          "start": 119.789, "duration": 4.03},
         {"text": "collapse into civil war. Sovereignty makes\nit hard for the international community to",
          "start": 123.819, "duration": 3.59},
         {"text": "intervene to stop either of those kinds of\nwars. But on the whole, when you see those",
          "start": 127.409, "duration": 3.711},
         {"text": "terrible headlines, remember the world's way\nbetter off than it ever has been. There's",
          "start": 131.12, "duration": 4.149},
         {"text": "less war and less violence than almost any\nother time in human history. ", "start": 135.269,
          "duration": 4.661}, {"text": "That's something worth celebrating.", "start": 139.93, "duration": 3.9}]
        transcript_json = json.dumps(transcript)
        start = 0
        end = 75
        get_transcript_score(transcript_json, start, end, users_tag_text)



