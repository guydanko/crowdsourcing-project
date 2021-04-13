from .views import video, create_tagging
from django.urls import path

urlpatterns = [
    path('videos/', video),
    path('create_tagging', create_tagging)
]

