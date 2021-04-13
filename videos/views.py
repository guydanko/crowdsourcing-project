from django.shortcuts import render, redirect
from .models import Video
from django.contrib import messages
from .forms import CreateNewTagging


# Create your views here.

def video(request):
    obj = Video.objects.all()
    form = CreateNewTagging()
    return render(request, 'video.html', {'obj': obj, 'form': form})


def create_tagging(response):
    if response.method == 'POST':
        form = CreateNewTagging(response.POST)
        if form.is_valid():
            form.save()
            print("Successfully saved the form in the db") #TODO debugging purposes to delete
        else:
            print("Failed to valid the form") # TODO Debugging
            messages.error(response, 'Invalid form')

    # redirecting back to video page
    return redirect('videos/')
