import datetime

from .models import *
from typing import List, Dict
from pandas import DataFrame
import pandas as pd
from django.core import serializers
from videos.tasks import get_transcript_score_async
from videos.tag_similarity import is_similar
from videos.Utils import _normalize_column, calculate_total_rating_score_for_tags

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

SIMILARITY_DELTA = 60


def get_all_videos() -> List[Video]:
    return Video.objects.all()


def get_user_by_id(user_id):
    return User.objects.get(id=user_id)


def get_tag_by_id(tag_id) -> Tagging:
    return Tagging.objects.get(id=tag_id)


def get_video_by_id(video_id) -> Video:
    return Video.objects.get(id=video_id)


def get_videos_containing_name(name) -> List[Video]:
    return Video.objects.filter(name__icontains=name)


def get_tags_for_video(video, user_id: int) -> List[Tagging]:
    return choose_which_tags_to_show(video, user_id)


def get_tags_for_video_in_time_range(video, start_seconds) -> List[Tagging]:
    return Tagging.objects.filter(video=video, start_seconds__range=(
        start_seconds - SIMILARITY_DELTA, start_seconds + SIMILARITY_DELTA))


def get_all_ratings_for_tag(tagging) -> List[UserRating]:
    return UserRating.objects.filter(tagging=tagging)


def get_user_rating_for_tag(creator, tagging) -> UserRating:
    return UserRating.objects.filter(creator=creator, tagging=tagging)


def get_rating_by_user_and_video(user, video) -> UserRating:
    return UserRating.objects.filter(creator=user, tagging__video=video)


def get_tags_active_for_user(user, tags) -> List[str]:
    user_rating_for_tags = []
    for tag in tags:
        try:
            is_upvote = get_user_rating_for_tag(user, tag)[0].is_upvote
            user_rating_for_tags.append(str(is_upvote))
        except IndexError:
            user_rating_for_tags.append("None")
    return user_rating_for_tags


def remove_user_rating_for_tag(creator, tagging) -> None:
    user_rating_list = get_user_rating_for_tag(creator=creator, tagging=tagging)
    if user_rating_list:
        user_rating = user_rating_list[0]
        if user_rating.is_upvote:
            tagging.up_votes -= 1
            tagging.rating_value -= 1
        else:
            tagging.down_votes -= 1
            tagging.rating_value += 1
        tagging.save()
        user_rating.delete()


def create_tag(video, user, start_time, end_time, description):
    errors = TaggingValidator.get_errors(creator=user, start=start_time, end=end_time, description=description,
                                         video=video)
    if errors:
        return errors

    tags_for_similarity_test = get_tags_for_video_in_time_range(video, time_to_seconds(start_time))
    for tag in tags_for_similarity_test:
        if is_similar(description, tag.description):
            return ['similar to an existing tag']
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)

    # get_transcript_score_async(video.transcript, user.id, start_time, end_time, description, video.id, start, end)  # sync

    get_transcript_score_async.delay(video.transcript, user.id, start_time, end_time, description, video.id,
                                     start_seconds, end_seconds)  # async


def create_user_rating(creator, tagging, is_upvote):
    errors = UserRatingValidator.get_errors(creator, tagging, is_upvote)
    if errors:
        return False
    remove_user_rating_for_tag(creator, tagging)
    user_rating = UserRating(creator=creator, tagging=tagging, is_upvote=is_upvote, video=tagging.video)
    if is_upvote:
        tagging.rating_value += 1
        tagging.up_votes += 1
    else:
        tagging.rating_value -= 1
        tagging.down_votes += 1
    tagging.save()
    user_rating.save()
    return True


def choose_which_tags_to_show(video, user_id: int) -> List[Tagging]:
    # creates df from the tags in order to put them in different time intervals buckets
    df = pd.DataFrame(list(Tagging.objects.filter(video=video).values(
        'rating_score', 'start_seconds', 'id', 'transcript_score', 'description', 'is_validated')))
    # TODO add function to compute similarity_delta
    df_user_ratings = pd.DataFrame(list(UserRating.objects.filter(creator=user_id, video=video).values('tagging')))
    if df_user_ratings.empty:
        df_user_ratings = pd.DataFrame({'tagging': []})
    print(f"this is my user id ----------------------------------------- {user_id}")
    print(df_user_ratings)
    df['bucket'] = (df['start_seconds'] / SIMILARITY_DELTA).astype(int)
    print(df)
    groups = df.groupby(by='bucket')
    tags_to_show = []
    # Iterate over each bucket and sort the values by total_tag_score and transcript score
    for key, grp in groups:
        grp = _normalize_column(grp, col_name='transcript_score')
        grp = calculate_total_rating_score_for_tags(grp)
        grp = grp.sort_values(by=['is_validated', 'total_tag_score', 'transcript_score'], ascending=False)
        print(grp)
        tags_to_show.extend(_pick_tags_from_time_interval(grp, df_user_ratings))

    return Tagging.objects.filter(id__in=tags_to_show).order_by('start__hour', 'start__minute', 'start__second')


def _pick_tags_from_time_interval(df: DataFrame, df_user_ratings: DataFrame) -> List[int]:
    validated_tags = 3
    random_validated = 2
    potential_tags = 3
    random_tail_tags = 2

    validated_df = df[df['is_validated']]
    not_val_not_vote = df[(~df['id'].isin(df_user_ratings['tagging']) & (df['is_validated'] == False))]
    # Case nothing to choose from
    if df.shape[0] <= 10:
        return list(df['id'])
    # Case we have enough validated
    elif validated_df.shape[0] >= validated_tags + random_validated:
        print('In first elif')
        v_tags = list(validated_df[:validated_tags]['id'])
        rnd_v_tags = list(validated_df[validated_tags:].sample(n=random_validated)['id'])
        pot_tags = list(not_val_not_vote[:min(potential_tags, not_val_not_vote.shape[0])]['id'])
        df_len = not_val_not_vote[len(pot_tags):].shape[0]
        rand_tags = list(not_val_not_vote[len(pot_tags):].sample(n=min(random_tail_tags, df_len))['id'])
        ids_to_show = v_tags + rnd_v_tags + pot_tags + rand_tags
        # If didn't populated 10 tags, then populate with tags didn't took with best scores
        if len(ids_to_show) < 10:
            rest_ids = df[~df['id'].isin(ids_to_show)]
            ids_to_show.extend(rest_ids[:10 - len(ids_to_show)]['id'])
        return ids_to_show
    # Case not enough validated
    else:
        print('In second elif')
        v_tags = list(validated_df['id'])  # took all validated
        diff = validated_tags + random_validated - len(v_tags)
        # took maximal amount of potential + the rest of validated
        pot_tags = list(not_val_not_vote[:min(potential_tags + diff, not_val_not_vote.shape[0])]['id'])
        ids_to_show = v_tags + pot_tags
        if len(pot_tags) == not_val_not_vote.shape[0]:
            rest_ids = df[~df['id'].isin(ids_to_show)]
            ids_to_show += rest_ids[:10 - len(ids_to_show)]['id']
            return ids_to_show
        else:
            df_len = not_val_not_vote[len(pot_tags):].shape[0]
            # pick random from tail
            ids_to_show += list(not_val_not_vote[len(pot_tags):].sample(n=min(random_tail_tags, df_len))['id'])
            if len(ids_to_show) < 10:
                ids_to_show += list(df[~df['ids'].isin(ids_to_show)]['id'])
            return ids_to_show


# Comment controllers
def get_all_comments_for_tag(tag) -> List[Comment]:
    return Comment.objects.filter(tag=tag)


def get_comment_by_id(comment_id) -> Comment:
    return Comment.objects.get(id=comment_id)


def get_serialized_comments_for_tag(tag) -> (Dict, int):
    comments = serializers.serialize('json', get_all_comments_for_tag(tag))
    if len(comments) == 2:
        status_code = 200
    else:
        status_code = 204
    return comments, status_code


def get_all_replies_for_comment(comment_id) -> List[Comment]:
    return Comment.objects.filter(parent_id=comment_id)
