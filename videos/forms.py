from django import forms
from django.forms import CharField, HiddenInput, widgets

from .models import Tagging


class VideoTaggingForm(forms.ModelForm):
    showAllTags = CharField(widget=HiddenInput(), required=False)
    # TimeTry = forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'))

    class Meta:
        model = Tagging
        exclude = ('creator', 'video', 'rating_value', 'date_subscribed')
        widgets = {
            'end': forms.TimeInput(format='%H:%M:%S'),
            'start': forms.TimeInput(format='%H:%M:%S'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["start"].widget.attrs.update({'input_type': 'time'})
        # self.fields["start"].input_formats = ['%H:%M:%S']
        # self.fields["start"].step = "2"
        # self.fields["end"].widget.attrs.update({'input_type': 'time'})
        self.fields["end"].widget = TimeInput()
        self.fields["start"].widget = TimeInput()


class TimeInput(forms.TimeInput):
    input_type = "time"



