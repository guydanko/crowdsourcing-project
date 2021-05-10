from django.shortcuts import render

from videos.models import Video


def index(request):
    obj = Video.objects.all()
    return render(request, 'layout/index.html', {'obj': obj})
