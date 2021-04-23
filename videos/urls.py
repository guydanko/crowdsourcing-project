from .views import video, vote
from django.urls import path

app_name = 'videos'

urlpatterns = [
    path('videos/<int:identifier>/', video, name='video'),
    path('videos/vote/', vote, name='vote')
]

