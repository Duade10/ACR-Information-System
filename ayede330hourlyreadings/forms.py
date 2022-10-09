from re import L
from django.utils import timezone
from django import forms
from . import models


def check_hour(hour):
    for hourly_reading in models.Ayede330ReadingSheet.objects.last().hourly_readings.all():
        if hour == hourly_reading.hour and timezone.now().day == hourly_reading.created.day:
            return False


class Ayede330HourlyReadingForm(forms.ModelForm):
    class Meta:
        model = models.Ayede330HourlyReading
        exclude = (
            "uploaded",
            "daily_area_load",
            "olorunsogo_mvar",
            "t2a_mvar",
            "user",
            "user_name",
            "t1a_kv",
            "t1a_mw",
            "t1a_a",
            "t1a_mvar",
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
