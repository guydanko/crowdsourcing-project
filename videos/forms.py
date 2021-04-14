from django import forms
from durationwidget.widgets import TimeDurationWidget

from .models import Tagging


class CreateNewTagging(forms.ModelForm):
    start = forms.DurationField(widget=TimeDurationWidget(
        show_days=False, show_hours=False, show_minutes=True, show_seconds=True
    ), required=True)
    end = forms.DurationField(widget=TimeDurationWidget(
        show_days=False, show_hours=False, show_minutes=True, show_seconds=True
    ), required=True)

    class Meta:
        model = Tagging
        exclude = ('date_subscribed',)
