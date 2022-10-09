from django import forms

from . import models


class TroublereportForm(forms.ModelForm):
    """Trouble Report of19 model form definition"""

    created_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = models.TroubleReport
        fields = (
            "to_authority",
            "department",
            "location",
            "location_of_trouble",
            "apparatus_in_trouble",
            "description_of_trouble",
            "description_of_switching",
            "created_at",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields["apparatus_in_trouble"].widget.attrs["class"] = "summernote-simple"
            self.fields["description_of_trouble"].widget.attrs["class"] = "summernote-simple"
            self.fields["description_of_switching"].widget.attrs["class"] = "summernote-simple"
            self.fields["to_authority"].label = "To"
            self.fields["description_of_trouble"].label = "Description of trouble (optional)"
            self.fields["description_of_switching"].label = "Description of switching (optional)"
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self, *args, **kwargs):
        trouble_report = super().save(commit=False)
        return trouble_report
