from django import forms
from django.forms import CharField, HiddenInput
from bootstrap_datepicker_plus import TimePickerInput
from .models import Tagging


class VideoTaggingForm(forms.ModelForm):
    """ Tag form configuration """
    showAllTags = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Tagging
        fields = ['start', 'end', 'description']

    def __init__(self, *args, **kwargs):
        super(VideoTaggingForm, self).__init__(*args, **kwargs)

        self.fields["end"].widget = TimePickerInput(format='%H:%M:%S')
        self.fields["end"].input_formats = ['%H:%M:%S']
        self.fields["end"].widget.attrs.update({'value': '00:00:00'})
        self.fields["start"].widget = TimePickerInput(format='%H:%M:%S')
        self.fields["start"].input_formats = ['%H:%M:%S']
        self.fields["start"].widget.attrs.update({'value': '00:00:00'})
        self.fields["start"].widget.config['options']['showTodayButton'] = False
        self.fields["start"].widget.config['options']['showClear'] = False
        self.fields["end"].widget.config['options']['showTodayButton'] = False
        self.fields["end"].widget.config['options']['showClear'] = False


class TimeInput(forms.TimeInput):
    input_type = "time"
