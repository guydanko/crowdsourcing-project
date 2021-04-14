from .views import all_videos, video
from django.urls import path

urlpatterns = [
    path('videos/', all_videos),
    path('videos/<int:identifier>/', video),
]

