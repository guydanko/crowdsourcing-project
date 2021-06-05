from .models import *

####--------GLOBALS---------####
TAGS_PER_VIDEO_AT_START = 10
ADD_TAGS_FOR_VALIDATION = 3
MAX_COMMENTS_PER_TAG = 3
MAX_REPLY_PER_COMMENT = 5
####------------------------####


def calculate_number_of_allowed_tags_per_video(video, user) -> int:
    """
    x := number of validated tags per the user
    total number of tags user can post--> f(x) = 10 + 3x
    """
    num_validated_tags = Tagging.objects.filter(creator=user, is_validated=True).count()
    num_of_tags_for_vid = Tagging.objects.filter(video=video, creator=user).count()
    tot_tags_user_can_post = TAGS_PER_VIDEO_AT_START + num_validated_tags * ADD_TAGS_FOR_VALIDATION
    return tot_tags_user_can_post - num_of_tags_for_vid


def is_user_able_to_post_comment_on_tag(user, tag) -> bool:
    num_of_comments_user_posted = Comment.objects.filter(tag=tag, creator=user, is_reply=False).count()
    return num_of_comments_user_posted < MAX_COMMENTS_PER_TAG


def is_user_able_to_post_reply_on_comment(user, tag, comment_id: int) -> bool:
    num_of_reply_user_posted_for_comment = Comment.objects.filter(parent=comment_id, creator=user, tag=tag).count()
    return num_of_reply_user_posted_for_comment < MAX_REPLY_PER_COMMENT
