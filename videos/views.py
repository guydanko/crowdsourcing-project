from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Video, Tagging
from django.contrib import messages
from .forms import CreateNewTagging


# Create your views here.

def all_videos(request):
    obj = Video.objects.all()
    form = CreateNewTagging()
    return render(request, 'videos/all_videos.html', {'obj': obj, 'form': form})


def video(request, identifier):
    obj = Video.objects.get(id=identifier)
    form = CreateNewTagging()
    tags = Tagging.objects.all()

    if request.method == 'POST':
        form = CreateNewTagging(request.POST)
        if form.is_valid():
            form.save()
            form = CreateNewTagging()
            print("Successfully saved the form in the db")  # TODO debugging purposes to delete
            HttpResponseRedirect('')
        else:
            print("Failed to valid the form")  # TODO Debugging
            messages.error(request, 'Invalid form')

    return render(request, 'videos/video.html', {'obj': obj, 'form': form, 'tags': tags})
