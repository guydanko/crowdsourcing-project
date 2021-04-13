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
            tagging.update(user_rating=tagging.rating_value - 1)
        else:
            tagging.update(user_rating=tagging.rating_value + 1)
        user_rating.delete()


def create_tagging():
    #TODO Omri
    pass


def create_user_rating(creator, tagging, is_upvote):
    remove_user_rating_for_tagging(creator, tagging)
    user_rating = UserRating(creator=creator, tagging=tagging)
    if is_upvote:
        tagging.update(user_rating=tagging.rating_value + 1)
    else:
        tagging.update(user_rating=tagging.rating_value - 1)
    user_rating.save()
