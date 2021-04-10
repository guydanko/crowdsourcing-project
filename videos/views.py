from django.shortcuts import render
from .models import Item


# Create your views here.

def video(request):
    obj = Item.objects.all()
    return render(request, 'video.html', {'obj': obj})
