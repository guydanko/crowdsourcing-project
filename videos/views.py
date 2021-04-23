from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
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
    return render(request, 'videos/video.html', {'obj': video, 'form': VideoTaggingForm(), 'tags': tags})


def vote(request):
    if request.method == 'POST':
        tag = get_tag_by_id(request.POST['tag_id'])
        is_upvote_string = request.POST['is_upvote']
        if is_upvote_string == "true":
            is_upvote = True
        else:
            is_upvote = False
        if create_user_rating(request.user, tag, is_upvote):
            response = HttpResponseRedirect('')
            response['Location'] = f'/videos/{tag.video.id}'
        else:
            response = HttpResponseNotAllowed()
        return response