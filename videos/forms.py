from django import forms
from .models import Tagging


class VideoTaggingForm(forms.ModelForm):
    class Meta:
        model = Tagging
        exclude = ('creator', 'video', 'rating_value', 'date_subscribed')
