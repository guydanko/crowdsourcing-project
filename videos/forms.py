from django import forms
from .models import Tagging


class VideoTaggingForm(forms.ModelForm):
    class Meta:
        model = Tagging
        fields = ['start', 'end', 'description']