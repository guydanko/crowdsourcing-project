import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from .models import Video, Tagging
from django.contrib import messages
from .forms import VideoTaggingForm, CommentForm
from .video_controller import *


# Create your views here.


def video(request, identifier):
    related_video = get_video_by_id(video_id=identifier)
    tags = get_all_tags_for_video(related_video)
    if request.method == 'POST':
        form = VideoTaggingForm(request.POST)
        if form.is_valid():
            # create a new model in the data base with the filled form information
            start_time = form.cleaned_data.get("start")
            end_time = form.cleaned_data.get("end")
            description = form.cleaned_data.get("description")
            create_tagging(related_video, request.user, start_time, end_time, description)
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, 'Invalid form')

    return render(request, 'videos/video.html', {'obj': related_video, 'form': VideoTaggingForm(), 'tags': tags,
                                                 'ratings_for_user': get_tags_active_for_user(request.user, tags)})


def vote(request):
    if request.method == 'POST':
        tag = get_tag_by_id(request.POST['tag_id'])
        is_upvote_string = request.POST['is_upvote']

        if is_upvote_string == "delete":
            remove_user_rating_for_tag(request.user, tag)
            return JsonResponse({'tag_rating': tag.rating_value}, status=200)

        if is_upvote_string == "true":
            is_upvote = True
        else:
            is_upvote = False

        if create_user_rating(request.user, tag, is_upvote):
            status_code = 201
        else:
            status_code = 405
        return JsonResponse({'tag_rating': tag.rating_value}, status=status_code)


def comment(request, video_id, tag_id):
    related_video = get_video_by_id(video_id)
    tag = get_tag_by_id(tag_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # if parent_id exists, then it's a reply
            try:
                parent_id = int(request.POST.get('parent_id'))
            except KeyError:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.tag = tag, new_comment.video = related_video
            new_comment.save()
    comments = get_all_comments_for_tag(tag)
    context = {'obj': related_video, 'comment_form': CommentForm(),
               'comments': comments}
    # need to edit from where it renders
    return render(request, 'videos/video.html', context)
