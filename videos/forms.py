from django import forms
from django.forms import CharField, HiddenInput

from .models import Tagging


class VideoTaggingForm(forms.ModelForm):
    showAllTags = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Tagging
        exclude = ('creator', 'video', 'rating_value', 'date_subscribed')



