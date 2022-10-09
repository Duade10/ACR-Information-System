from django import forms

from . import models


class FeederForm(forms.ModelForm):
    class Meta:
        model = models.Feeder
        fields = ("name", "station_132")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
