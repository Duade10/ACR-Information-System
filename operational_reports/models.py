from core.models import AbstractTimeStampedModel
from django.db import models

"""
EVENT/ INDICATION

# FORCED :CLASS
Isnt EF (DISCO)
132LN TRIO
330LN TRIP
330TRF TRIP
CB F
EF(DISCO)
EF(TCN)
HIGH OIL TEMP
'' WIND TEMP
INST EF (TCN)
INST OC (DISCO)
'' OC/EF (DISCO)
'' ''    (TCN)
NO RELAY IND
OC (DISCO)
'' (TCN)
REF
SBEF
SYS COLL
TRF BUCHHOLZ
TRF DIFF TRIP
TRF SEC EF (DISCO)
TRF SEC EF (TCN)
TRF SEC OC (DISCO)
TRF SEC OC (TCN)
# PLANNED :CLASS
DISCO MAINT.
TCN MAINT.
# EMRG :CLASS
EMRG (DISCO)
EMRG (TCN)
L/SHED (G/S)
TRF LIM
LINE LIM
132KV U/FREQ OP
33KV U/FREQ OP
"""


class OperationalReport(AbstractTimeStampedModel):
    """Operational Report Model Definition"""

    LOAD_SHEDDING = "l/s"
    EARTH_FAULT = "e/f"
    OVER_CURRENT = "o/c"
    EARTH_FAULT_AND_OVER_CURRENT = "e/f&o/c"

    REASON_CHOICES = (
        (LOAD_SHEDDING, "Load Shedding"),
        (EARTH_FAULT, "Earth Fault"),
        (OVER_CURRENT, "Over Current"),
        (EARTH_FAULT_AND_OVER_CURRENT, "Earth Fault / Over Current"),
    )

    YELLOW_PHASE = "y"
    YELLOW_AND_BLUE_PHASE = "y&b"
    BLUE_PHASE = "b"
    BLUE_AND_RED_PHASE = "b&r"
    RED_PHASE = "r"
    RED_AND_YELLOW_PHASE = "r&y"
    ALL_PHASES = "r,y&b"

    PHASE_CHOICES = (
        (YELLOW_PHASE, "Yellow Phase"),
        (BLUE_PHASE, "Blue Phase"),
        (RED_PHASE, "Red Phase"),
        (YELLOW_AND_BLUE_PHASE, "Yellow and Blue Phase"),
        (BLUE_AND_RED_PHASE, "Blue and Red Phase"),
        (RED_AND_YELLOW_PHASE, "Red and Yellow Phase"),
        (ALL_PHASES, "All Phases"),
    )

    from_time = models.IntegerField(null=True, blank=True)
    to_time = models.IntegerField(null=True, blank=True)
    feeder = models.ForeignKey("feeders.Feeder", on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=8, choices=REASON_CHOICES, null=True, blank=True)
    phase = models.CharField(max_length=7, choices=PHASE_CHOICES, null=True, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    user_name = models.CharField(max_length=50)
    load_loss = models.IntegerField(null=True, blank=True)
    dispatch = models.CharField(max_length=40, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    station_132 = models.ForeignKey(
        "stations_132.Station_132",
        on_delete=models.CASCADE,
        related_name="operational_reports",
        null=True,
        blank=True,
    )
    station_132_330 = models.ForeignKey(
        "stations_330.Station_330",
        on_delete=models.CASCADE,
        related_name="operational_reports",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = self.user.get_full_name()
            self.station_132 = self.user.station_132
            self.station_132_330 = self.user.station_132.station_330

        if self.reason == "l/s":
            self.content = f"was opened on load shedding; Frequency ({self.frequency})"
        elif self.reason == "e/f":
            self.content = f"tripped on earth fault (e/f) {str(self.phase).upper()} phase"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_name
