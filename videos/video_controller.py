from videos.models import Video, Tagging, UserRating


def get_all_videos():
    return Video.objects.all()


def get_all_taggings_for_video(video):
    return Tagging.objects.filter(video=video)


def get_all_ratings_for_tagging(tagging):
    return UserRating.objects.filter(tagging=tagging)


def get_user_rating_for_tagging(creator, tagging):
    return UserRating.objects.filter(creator=creator, tagging=tagging)


def remove_user_rating_for_tagging(creator, tagging):
    user_rating_list = get_user_rating_for_tagging(creator=creator, tagging=tagging)
    if user_rating_list:
        user_rating = user_rating_list[0]
        if user_rating.is_upvote:
            tagging.rating_value -= 1
        else:
            tagging.rating_value += 1
        tagging.save()
        user_rating.delete()


def create_tagging(video, user, start_time, end_time, description):
    tag = Tagging.objects.create(creator=user, start=start_time, end=end_time,
                                 description=description, video=video)
    tag.save()


def create_user_rating(creator, tagging, is_upvote):
    remove_user_rating_for_tagging(creator, tagging)
    user_rating = UserRating(creator=creator, tagging=tagging, is_upvote=is_upvote)
    if is_upvote:
        tagging.rating_value += 1
    else:
        tagging.rating_value -= 1
    tagging.save()
    user_rating.save()
