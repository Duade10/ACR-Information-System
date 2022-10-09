from django import forms

from . import models


class SheetModelForm(forms.ModelForm):
    """Abstrack Sheet Model Form Definition"""

    class Meta:
        model = models.AbstractSheetModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
