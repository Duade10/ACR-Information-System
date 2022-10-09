from django.utils import timezone
from django import forms
from . import models


def check_hour(hour):
    for hourly_reading in models.Ayede132ReadingSheet.objects.last().hourly_readings.all():
        if hour == hourly_reading.hour and timezone.now().day == hourly_reading.created.day:
            return False


class Ayede132HourlyReadingForm(forms.ModelForm):
    class Meta:
        model = models.Ayede132HourlyReading
        exclude = (
            "uploaded",
            "user",
            "user_name",
            "spare",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        h = timezone.now() + timezone.timedelta(hours=1)
        hour = f"{h.hour}00"
        for field in self.fields:
            self.fields["hour"].initial = hour
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self, *args, **kwargs):
        reading = super().save(commit=False)
        return reading
