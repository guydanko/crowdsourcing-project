from django.urls import path

from . import views

app_name = 'layout'

urlpatterns = [
    path('', views.index, name='index'),
]
