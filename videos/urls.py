from .views import video
from django.urls import path
app_name = 'videos'
urlpatterns = [
    path('videos/<int:identifier>/',video, name='video'),
]

