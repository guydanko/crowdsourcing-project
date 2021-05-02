from .views import video, vote, search_videos, view_comments, create_comment, delete_comment
from django.urls import path

app_name = 'videos'

urlpatterns = [
    path('videos/<int:identifier>/', video, name='video'),
    path('videos/vote/', vote, name='vote'),
    path('videos/search/', search_videos, name='search'),
    path('videos/comments/', view_comments, name='comment'),
    path('videos/create_comment/', create_comment, name='create_comment'),
    path('videos/delete_comment/', delete_comment, name='delete_comment'),
]
