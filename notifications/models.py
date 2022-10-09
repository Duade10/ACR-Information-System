from django.db import models
from core.models import AbstractTimeStampedModel


class Notification(AbstractTimeStampedModel):
    url = models.CharField(null=True, blank=True, max_length=132)
    icon = models.CharField(max_length=5, null=True, blank=True)
    text = models.CharField(max_length=500)
    to_user = models.ForeignKey(
        "users.User",
        related_name="notifications_to",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    from_user = models.ForeignKey(
        "users.User",
        related_name="notifications_from",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    from_station_330 = models.ForeignKey(
        "stations_330.Station_330",
        related_name="notifications_from",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    from_station_132 = models.ForeignKey(
        "stations_132.Station_132",
        related_name="notifications_from",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    to_station_132 = models.ManyToManyField(
        "stations_132.Station_132",
        related_name="notifications_to",
        blank=True,
    )
    to_station_330 = models.ManyToManyField(
        "stations_330.Station_330",
        related_name="notifications_to",
        blank=True,
    )

    user_has_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"
