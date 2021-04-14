from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Video, Tagging
from django.contrib import messages
from .forms import CreateNewForm
from .video_controller import *


# Create your views here.

def all_videos(request):
    obj = Video.objects.all()
    form = CreateNewForm()
    return render(request, 'videos/all_videos.html', {'obj': obj, 'form': form})


def video(request, identifier):
    obj = Video.objects.get(id=identifier)
    form = CreateNewForm()
    tags = get_all_taggings_for_video(identifier)
    if request.method == 'POST':
        form = CreateNewForm(request.POST)
        if form.is_valid():
            # create a new model in the data base with the filled form information
            start_time = form.cleaned_data.get("start")
            end_time = form.cleaned_data.get("end")
            description = form.cleaned_data.get("description")
            tag = Tagging.objects.create(related_user=request.user, start=start_time, end=end_time,
                                         description=description, related_video=identifier)
            tag.save()
            HttpResponseRedirect('')
        else:
            messages.error(request, 'Invalid form')
    return render(request, 'videos/video.html', {'obj': obj, 'form': form, 'tags': tags})
