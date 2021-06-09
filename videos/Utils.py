import math
from datetime import datetime as dt
import datetime


# Configurations :
date = datetime.date(1, 1, 1)

####--------GLOBALS---------####
MIN_INTERVAL_LENGTH = 60  # seconds
INVALID_THRESHOLD = (1 / 3)
TOTAL_VOTES_FOR_INVALIDATION = 50
####------------------------####

def rating_score_calc(ups: int, downs: int) -> float:
    """ Using variation of Reddit comment rating algorithm to calculate likes/dislikes score
        based on Wilson's confidence interval lower bound"""
    n = ups + downs
    if n == 0:
        return 0
    z = 1.96  # confidence of 0.95%
    phat = float(ups) / n
    return round((phat + z * z / (2 * n) - z *
                  math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n), 10)


def calculate_total_rating_score_for_tag(rating_score: float, transcript_score: float) -> float:
    """ Calculates the total rating score for a tag, a function f(x,y) = x*0.9 + y*0.1"""
    weights = [0.9, 0.1]
    return rating_score * weights[0] + transcript_score * weights[1]


def compute_video_bucket_length(length_seconds: int) -> int:
    """ Computes the video bucket length, by the following function :
        f(x) = x.length / log(x.length) / 2 so for example:
        video length of 60 minutes have buckets of size 506 seconds,
        video length of 15 minutes have buckets of size 152 seconds"""
    bucket_length = round((float(length_seconds) / (math.log(length_seconds, 10) * 1.5)))
    return max(bucket_length, MIN_INTERVAL_LENGTH)


def is_tag_invalid(up_votes: int, down_votes: int) -> bool:
    """ Returns if the tag turned invalid by checking if the number of down votes is 3x or more
        then the number of up votes given by the total amount of votes is > 50 """
    return (float(up_votes) / float(max(down_votes, 1))) < INVALID_THRESHOLD \
           and (up_votes + down_votes) > TOTAL_VOTES_FOR_INVALIDATION


def seconds_to_time(duration_in_seconds):
    hours = duration_in_seconds // 3600
    minutes = (duration_in_seconds % 3600) // 60
    seconds = duration_in_seconds % 60
    return datetime.time(hours, minutes, seconds)


def time_to_seconds(time_object):
    return time_object.hour * 3600 + time_object.minute * 60 + time_object.second