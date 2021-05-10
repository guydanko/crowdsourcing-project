import json

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.contrib import messages
from rest_framework.decorators import api_view
from .forms import VideoTaggingForm
from .video_controller import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def video(request, identifier):
    video = get_video_by_id(video_id=identifier)
    tags = get_all_tags_for_video(video)
    user_tags = get_all_user_tags_for_video(user_id=request.user.id, video_id=identifier)
    show_all_tags = True
    if request.method == 'GET':
        if 'showAllTags' in request.GET:
            if request.GET['showAllTags'] == "True":
                show_all_tags = True
            else:
                show_all_tags = False
    if request.method == 'POST':
        form = VideoTaggingForm(request.POST)
        if form.is_valid():
            # create a new model in the data base with the filled form information
            start_time = form.cleaned_data.get("start")
            end_time = form.cleaned_data.get("end")
            description = form.cleaned_data.get("description")
            create_tagging(video, request.user, start_time, end_time, description)
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, 'Invalid form')

    return render(request, 'videos/video.html',
                  {'obj': video, 'form': VideoTaggingForm(), 'tags': tags, 'user_tags': user_tags,
                   'show_all_tags': show_all_tags,
                   'ratings_for_user': get_tags_active_for_user(request.user, tags)})


def vote(request):
    if request.method == 'POST':
        tag = get_tag_by_id(request.POST['tag_id'])
        is_upvote_string = request.POST['is_upvote']

        if is_upvote_string == "delete":
            remove_user_rating_for_tag(request.user, tag)
            return JsonResponse({'tag_rating': tag.rating_value}, status=200)

        if is_upvote_string == "true":
            is_upvote = True
        else:
            is_upvote = False

        if create_user_rating(request.user, tag, is_upvote):
            status_code = 201
        else:
            status_code = 405
        return JsonResponse({'tag_rating': tag.rating_value}, status=status_code)


def delete_tag(request):
    if request.method == 'POST':
        tag_id = request.POST['tag_id']

        remove_user_tag(tag_id=tag_id)
        status_code = 200

        return JsonResponse({}, status=status_code)


def search_videos(request):
    if request.method == 'GET':
        search_term = request.GET['search_term']
        videos = get_videos_containing_name(search_term)

        if videos:
            status_code = 200
        else:
            status_code = 204

        json_videos = serializers.serialize('json', videos)
        return JsonResponse({'videos': json_videos}, status=status_code)


# -------------------------- Comment views -------------------------------------

@csrf_exempt
@api_view(['POST'])
def create_comment(request):
    if request.method == 'POST':
        data = request.POST
        tag = get_tag_by_id(data['tag_id'])
        comment_body = data['body']
        if len(comment_body) > 400:
            messages.error(request, 'Comment text exceeded maximum length')
        else:
            comment = Comment(body=comment_body, tag=tag, video=tag.video,
                              create=User.objects.get(id=request.user.id))
            parent_id = int(data['parent_id']) if 'parent_id' in data else None
            if parent_id:
                # reply comment
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
                comment.is_reply = True
            comment.save()
            messages.success(request, 'Comment saved successfully')

        comments, status_code = get_serialized_comments_for_tag(tag)
        return JsonResponse({'comments_list': comments}, status=status_code)


@csrf_exempt
@api_view(['POST'])
def delete_comment(request):
    if request.method == 'POST':
        tag = get_tag_by_id(request.POST['tag_id'])
        comment = get_comment_by_id(request.POST['comment_id'])
        if comment.creator.id == request.user.id:
            try:
                comment.delete()
            except AttributeError:
                messages.warning(request, 'The comment could not be deleted.')
        else:
            messages.warning(request, 'Only comment owner can delete')
        comments, status_code = get_serialized_comments_for_tag(tag)
        return JsonResponse({'comments_list': comments}, status=status_code)


@csrf_exempt
@api_view(['POST'])
def view_comments(request):
    if request.method == 'POST':
        tag = get_tag_by_id(request.POST['tag_id'])
        comments, status_code = get_serialized_comments_for_tag(tag)
        return JsonResponse({'tag_id': tag.id, 'comments_list': comments}, status=status_code)
