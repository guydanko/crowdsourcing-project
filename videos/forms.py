from django import forms
from .models import Tagging


class CreateNewTagging(forms.ModelForm):

    class Meta:
        model = Tagging
        exclude = ('date_subscribed',)

