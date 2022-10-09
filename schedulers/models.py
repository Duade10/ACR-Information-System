from core.models import AbstractTimeStampedModel
from django.db import models


class ScheduledReport(AbstractTimeStampedModel):
    """Scheduled Reports Model For Reports That Needs Reminder"""

    protection_guarantee = models.ForeignKey(
        "protection_guarantees.ProtectionGuarantee", on_delete=models.CASCADE, null=True, blank=True
    )
    broadcast_on = models.DateField(null=True, blank=True)
    is_displayed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.broadcast_on = self.protection_guarantee.to_be_issued
        super().save(*args, **kwargs)

    def __str__(self):
        return self.protection_guarantee

    def get_protection_guarantee_s_report(self):
        try:
            if self.protection_guarantee.applied_to_132:
                station = f"{self.protection_guarantee.applied_to_132}"
                station_id = self.protection_guarantee.applied_to_132.id
                station_132_330_id = self.protection_guarantee.applied_to_132_330.id
            if self.protection_guarantee.applied_to_330:
                station = f"{self.protection_guarantee.applied_to_330}"
                station_id = self.protection_guarantee.applied_to_330.id
                station_132_330_id = 0
            return dict(
                name=self.protection_guarantee.user_name,
                time=f"{self.protection_guarantee.to_be_issued_at.hour}:{self.protection_guarantee.to_be_issued_at.minute}",
                for_a=self.protection_guarantee.for_a,
                station=station,
                stationId=station_id,
                station330Id=station_132_330_id,
                time_from=f"{self.protection_guarantee.to_be_issued_at.hour}{self.protection_guarantee.to_be_issued_at.minute}",
                time_to=f"{self.protection_guarantee.to_be_surrendered_at.hour}{self.protection_guarantee.to_be_surrendered_at.minute}",
                bool=True,
                url=self.protection_guarantee.get_absolute_url(),
            )
        except Exception:
            pass
