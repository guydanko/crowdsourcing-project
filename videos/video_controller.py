from typing import List, Dict
import pandas as pd
from pandas import DataFrame
from django.core import serializers
from videos.tasks import update_transcript_score_async
from videos.tag_similarity import is_similar
from .spammers import *

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


def get_all_user_tags_for_video(user_id, video_id) -> List[Tagging]:
    up_voted_tags_for_vid = UserRating.objects.filter(creator__id=user_id, video_id=video_id, is_upvote=True)
    tags_user_liked = [rating.tagging for rating in up_voted_tags_for_vid]
    tags_created_by_user = Tagging.objects.filter(creator__id=user_id, video_id=video_id)
    total_list = []
    for tag in tags_created_by_user:
        total_list.append(tag)
    total_list += tags_user_liked
    total_list.sort(key=lambda x: (x.start_seconds, -x.total_tag_score))
    return total_list


def get_all_ratings_for_tag(tagging) -> List[UserRating]:
    return UserRating.objects.filter(tagging=tagging)


def get_user_rating_for_tag(creator, tagging) -> UserRating:
    return UserRating.objects.filter(creator=creator, tagging=tagging)


def get_rating_by_user_and_video(user, video) -> UserRating:
    return UserRating.objects.filter(creator=user, tagging__video=video)


def get_tags_active_for_user(user, tags) -> List[str]:
    """ Returns upvote/downvote info for the displayed tags """
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


def remove_user_tag(tag_id):
    get_tag_by_id(tag_id).delete()


def create_tag(video, user, start_time, end_time, description):
    # input validation
    errors = TaggingValidator.get_errors(creator=user, start=start_time, end=end_time, description=description,
                                         video=video)
    if errors:
        return errors
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)
    # get the existing tags in the relevant time range
    tags_for_similarity_test = get_tags_for_video_in_time_range(video, start_seconds)
    for tag in tags_for_similarity_test:
        if is_similar(description, tag.description):
            # if tag is similar to an existing tags, adds it as an invalid tag,
            # which will only be displayed to the creator
            tag = Tagging.objects.create(creator=user, start=start_time, start_seconds=start_seconds, end=end_time,
                                         end_seconds=end_seconds, description=description, video=video, is_invalid=True)
            tag.save()
            return ['similar to an existing tag']

    # tag passed all the validations and is ready to receive a transcript score.
    # the tag will be saved and a valid tag with transcript score 0
    # the transcript score will be updated when the model finishes calculating it
    tag = Tagging.objects.create(creator=user, start=start_time, start_seconds=start_seconds, end=end_time,
                                 end_seconds=end_seconds, description=description, video=video, is_invalid=False)
    tag.save()
    # the function will run asynchronously, brokered by RabbitMQ and managed by Celery
    update_transcript_score_async.delay(video.transcript, description, start_seconds, end_seconds, tag.id)


def create_user_rating(creator, tag, is_upvote):
    errors = UserRatingValidator.get_errors(creator, tag, is_upvote)
    if errors:
        return False
    remove_user_rating_for_tag(creator, tag)
    user_rating = UserRating(creator=creator, tagging=tag, is_upvote=is_upvote, video=tag.video)
    if is_upvote:
        tag.rating_value += 1
        tag.up_votes += 1
    else:
        tag.rating_value -= 1
        tag.down_votes += 1
    tag.save()
    user_rating.save()
    return True


def choose_which_tags_to_show(video, user_id: int) -> List[Tagging]:
    # Step 1 - Create data frames
    df = pd.DataFrame(list(Tagging.objects.filter(video=video, is_invalid=False).values(
        'rating_score', 'start_seconds', 'id', 'transcript_score', 'description', 'is_validated', 'total_tag_score')))
    df_user_ratings = pd.DataFrame(list(UserRating.objects.filter(creator=user_id, video=video).values('tagging')))
    if df.empty:
        return []
    if df_user_ratings.empty:
        df_user_ratings = pd.DataFrame({'tagging': []})
    # Step 2 - split to intervals and get top tags per time interval
    df['bucket'] = (df['start_seconds'] / video.bucket_size).astype(int)
    df['Show_Tag'] = 0
    df = df.groupby(by='bucket').apply(_pick_tags_from_time_interval, df_user_ratings=df_user_ratings)
    # Step 3 - Take id's which has been decided to being showed up for the user
    tags_to_show = df[df['Show_Tag'] == 1]['id']
    return Tagging.objects.filter(id__in=tags_to_show).order_by('start__hour', 'start__minute', 'start__second',
                                                                '-total_tag_score')


def _pick_tags_from_time_interval(df: DataFrame, df_user_ratings: DataFrame) -> DataFrame:
    # Init default params
    validated_tags = 3
    random_validated = 2
    potential_tags = 3
    random_tail_tags = 2
    total_tags = 10

    df = df.sort_values(by=['is_validated', 'total_tag_score', 'transcript_score'], ascending=False)
    validated_df = df[df['is_validated']]
    not_val_not_vote = df[(~df['id'].isin(df_user_ratings['tagging']) & (df['is_validated'] == False))]

    # Case nothing to choose from
    if df.shape[0] <= total_tags:
        df['Show_Tag'] = 1
        return df
    # Case we have enough validated
    elif validated_df.shape[0] >= validated_tags + random_validated:
        v_tags = list(validated_df[:validated_tags]['id'])
        rnd_v_tags = list(validated_df[validated_tags:].sample(n=random_validated)['id'])
        pot_tags = list(not_val_not_vote[:min(potential_tags, not_val_not_vote.shape[0])]['id'])
        df_len = not_val_not_vote[len(pot_tags):].shape[0]
        rand_tags = list(not_val_not_vote[len(pot_tags):].sample(n=min(random_tail_tags, df_len))['id'])
        ids_to_show = v_tags + rnd_v_tags + pot_tags + rand_tags
        # If didn't found enough potential tags and enough random tags from the set of tags that aren't validated
        # and aren't voted by the user, the fill the remaining slots with top tags from the rest of the tags.
        if len(ids_to_show) < total_tags:
            rest_ids = df[~df['id'].isin(ids_to_show)]
            ids_to_show.extend(rest_ids[:total_tags - len(ids_to_show)]['id'])
    # Case not enough validated
    else:
        v_tags = list(validated_df['id'])  # took all validated
        diff = validated_tags + random_validated - len(v_tags)
        # took maximal amount of potential + the rest of validated
        pot_tags = list(not_val_not_vote[:min(potential_tags + diff, not_val_not_vote.shape[0])]['id'])
        ids_to_show = v_tags + pot_tags
        if len(pot_tags) == not_val_not_vote.shape[0]:
            rest_ids = df[~df['id'].isin(ids_to_show)]
            ids_to_show += list(rest_ids[:total_tags - len(ids_to_show)]['id'])

        else:
            df_len = not_val_not_vote[len(pot_tags):].shape[0]
            # pick random from tail
            ids_to_show += list(not_val_not_vote[len(pot_tags):].sample(n=min(random_tail_tags, df_len))['id'])
            if len(ids_to_show) < total_tags:
                ids_to_show += list(df[~df['id'].isin(ids_to_show)]['id'])

    # Mark all tags we decided to show with 1 the rest by default are 0
    df.loc[df['id'].isin(ids_to_show), 'Show_Tag'] = 1
    return df


# Comment controllers

def get_all_comments_for_tag(tag) -> List[Comment]:
    return Comment.objects.filter(tag=tag)


def get_comment_by_id(comment_id) -> Comment:
    return Comment.objects.get(id=comment_id)


def get_serialized_comments_for_tag(tag) -> (Dict, int):
    comments = serializers.serialize('json', get_all_comments_for_tag(tag))
    if len(comments) == 2:
        status_code = 204
    else:
        status_code = 201
    return comments, status_code


def get_all_replies_for_comment(comment_id) -> List[Comment]:
    return Comment.objects.filter(parent_id=comment_id)
