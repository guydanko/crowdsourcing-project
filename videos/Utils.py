import math
from pandas import DataFrame

####--------GLOBALS---------####
MIN_INTEVAL_SIZE = 60  # seconds
####------------------------####

def rating_score_calc(ups: int, downs: int) -> float:
    # Using variation of Reddit comment rating algorithm based on lower bound of Wilson's confidence interval.
    n = ups + downs
    if n == 0:
        return 0
    z = 1.96  # confidence of 0.95%
    phat = float(ups) / n
    return round((phat + z * z / (2 * n) - z *
                  math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n), 10)


def calculate_total_rating_score_for_tags(df: DataFrame) -> DataFrame:
    # Calculates the total score for each tag and inserting it to data frame column
    weights = [0.9, 0.1]
    df['total_tag_score'] = df['rating_score'] * weights[0] + df['normalize_transcript_score'] * weights[1]
    return df


def calculate_total_rating_score_for_tag(rating_score: float, transcript_score: float) -> float:
    # TODO there is an issue here as transcript_score is not normalized and can be very high,
    #  those the rating_score will be less impactful
    weights = [0.9, 0.1]
    return rating_score * weights[0] + transcript_score * weights[1]


def _normalize_column(df: DataFrame, col_name: str) -> DataFrame:
    # Min-Max normalize given column and assign values to new data frame column
    min_val = df[col_name].min()
    max_val = df[col_name].max()
    if min_val == max_val:
        df[f"normalize_{col_name}"] = 0
    else:
        df[f"normalize_{col_name}"] = ((df[col_name] - min_val) / (max_val - min_val))
    return df


def compute_video_bucket_length(length_seconds: int) -> int:
    bucket_length = round(length_seconds / math.log(length_seconds))
    return max(bucket_length, MIN_INTEVAL_SIZE)
