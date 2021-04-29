from django import forms
from .models import Tagging, Comment


class VideoTaggingForm(forms.ModelForm):
    class Meta:
        model = Tagging
        exclude = ('creator', 'video', 'rating_value', 'date_subscribed')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)