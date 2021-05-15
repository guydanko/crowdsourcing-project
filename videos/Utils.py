import math
import numpy as np
import pandas as pd
from pandas import DataFrame


def rating_score_calc(ups: int, downs: int) -> float:
    # Using variation of Reddit comment rating algorithm based on lower bound of the confidence interval.

    n = ups + downs
    if n == 0:
        return 0
    z = 1.96  # confidence of 0.95%
    phat = float(ups) / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


def calculate_total_rating_score_for_tags(df: DataFrame) -> DataFrame:
    """
    Given data frame consist tags for video, it generates total_tag_score column
    that consist the aggregated rating score from 2 measurements, rating_score and normalize_transcript_score
    :param df:
    :return: same df with the new column total_tag_score
    """
    weights = [0.9, 0.1]
    df['total_tag_score'] = df['rating_score'] * weights[0] + df['normalize_transcript_score'] * weights[1]
    return df


def calculate_total_rating_score_for_tag(rating_score: float, transcript_score: float) -> float:
    weights = [0.9, 0.1]
    return rating_score * weights[0] + transcript_score * weights[1]


def _normalize_column(df: DataFrame, col_name: str) -> DataFrame:
    """
    Given Data frame it min-max normalize it's col_name inserting to new column
    must be numerical column
    :param df:
    :param col_name:
    :return: Same df with normalized_col_name column
    """
    min_val = df[col_name].min()
    max_val = df[col_name].max()
    if min_val == max_val:
        df[f"normalize_{col_name}"] = 0
    else:
        df[f"normalize_{col_name}"] = ((df[col_name] - min_val) / (max_val - min_val))
    return df
