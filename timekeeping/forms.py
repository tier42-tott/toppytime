from django.forms import ModelForm, DateTimeInput, ValidationError
from timekeeping.models import TimeEntry


class CustomDateTimeWidget(DateTimeInput):
    input_type = 'datetime-local'


class TimeEntryForm(ModelForm):
    class Meta:
        model = TimeEntry
        fields = '__all__'
        widgets = {
            'start_time': CustomDateTimeWidget,
            'end_time': CustomDateTimeWidget,
        }

    def clean(self):
        cleaned_data = super(TimeEntryForm, self).clean()

        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']

        if start_time >= end_time:
            raise ValidationError('Start Time must be before End Time!')

        return cleaned_data
