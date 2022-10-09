from django import forms

from . import models


class ProtectionGuaranteeForm(forms.ModelForm):
    """Protection Guarantee Model Form Definition"""

    to_be_issued = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    to_be_issued_at = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    to_be_surrendered_at = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
    apparatus_outage_to = forms.DateTimeField(required=False, widget=forms.TextInput())
    switching_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    final_approval_at = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={"type": "datetime-local"}))

    class Meta:
        model = models.ProtectionGuarantee
        exclude = (
            "approved_by_name",
            "user_name",
            "slug",
            "applied_to_132_330",
            "user",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields["description_of_apparatus"].widget.attrs["class"] = "summernote-simple"
            self.fields["additional_apparatus"].widget.attrs["class"] = "summernote-simple"
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self):
        protection_guarantee = super().save(commit=False)
        print("NAME: ", protection_guarantee.user)
        return protection_guarantee
