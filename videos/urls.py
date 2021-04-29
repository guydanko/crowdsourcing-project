from .views import video, vote, search_videos
from django.urls import path

app_name = 'videos'

urlpatterns = [
    path('videos/<int:identifier>/', video, name='video'),
    path('videos/vote/', vote, name='vote'),
    path('videos/search/', search_videos, name='search')
]
