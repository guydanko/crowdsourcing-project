from django import forms
from django.forms import CharField, HiddenInput, TimeInput

from .models import Tagging


class VideoTaggingForm(forms.ModelForm):
    showAllTags = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Tagging
        # exclude = ('creator', 'video', 'rating_value', 'date_subscribed')
        fields = ['start', 'end', 'description']

    def __init__(self, *args, **kwargs):
        super(VideoTaggingForm, self).__init__(*args, **kwargs)

        self.fields["end"].widget = TimeInput()
        self.fields["end"].widget.attrs.update({'step': '1'})
        self.fields["start"].widget = TimeInput()
        self.fields["start"].widget.attrs.update({'step': '1'})


class TimeInput(forms.TimeInput):
    input_type = "time"

    # def __init__(self, **kwargs):
    #     kwargs["format"] = "%H:%M:%S"
    #     super().__init__(**kwargs)


