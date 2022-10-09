from django import forms
from feeders import models as feeders_models

from . import models


class OperationalReportForm(forms.ModelForm):
    """Operational Report Model Form Definition"""

    class Meta:
        model = models.OperationalReport
        exclude = ("user_name", "user", "station_132", "station_132_330", "content")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.designation == "330":
            station = None
        if user.designation == "132":
            station = user.station_132
        for field in self.fields:
            self.fields["feeder"].queryset = feeders_models.Feeder.objects.filter(station_132=station)
            self.fields["frequency"].widget.attrs["placeholder"] = "00.00"
            self.fields[field].widget.attrs["class"] = "form-control"
