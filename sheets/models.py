from core.models import AbstractTimeStampedModel
from django.db import models


class AbstractSheetModel(AbstractTimeStampedModel):
    """Sheet Model for Google Sheets. Abstract is set to True, so as not to create fields in database"""

    google_sheet_title = models.CharField(max_length=60)
    google_sheet_id = models.CharField(max_length=200)

    class Meta:
        abstract = True
