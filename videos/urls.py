from .views import video, vote, comment
from django.urls import path

app_name = 'videos'

urlpatterns = [
    path('videos/<int:identifier>/', video, name='video'),
    path('videos/vote/', vote, name='vote'),
    path('videos/<int:video_id>/comments_<int:tag_id>/', comment, name='comment'),
]

