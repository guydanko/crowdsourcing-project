import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from .models import Video, Tagging
from django.contrib import messages
from .forms import VideoTaggingForm
from .video_controller import *


# Create your views here.


def video(request, identifier):
    video = get_video_by_id(video_id=identifier)
    tags = get_all_tags_for_video(video)
    if request.method == 'POST':
        form = VideoTaggingForm(request.POST)
        if form.is_valid():
            # create a new model in the data base with the filled form information
            start_time = form.cleaned_data.get("start")
            end_time = form.cleaned_data.get("end")
            description = form.cleaned_data.get("description")
            create_tagging(video, request.user, start_time, end_time, description)
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, 'Invalid form')

    # TODO generate a list of the user ratings for each tag in the video (if they exist)
    user_rating_for_tags = []
    for tag in tags:
        try:
            is_upvote = get_user_rating_for_tagging(request.user, tag)[0].is_upvote
            user_rating_for_tags.append(str(is_upvote))
        except IndexError:
            user_rating_for_tags.append("None")

    return render(request, 'videos/video.html', {'obj': video, 'form': VideoTaggingForm(), 'tags': tags,
                                                 'ratings_for_user': user_rating_for_tags})


def vote(request):
    if request.method == 'POST':
        tag = get_tag_by_id(request.POST['tag_id'])
        is_upvote_string = request.POST['is_upvote']
        if is_upvote_string == "true":
            is_upvote = True
        else:
            is_upvote = False
        if create_user_rating(request.user, tag, is_upvote):
            context = {'tag_rating': tag.rating_value}
            response = JsonResponse(context, status=200)
        else:
            context = {'tag_rating': tag.rating_value}
            response = JsonResponse(context, status=405)
        return response
