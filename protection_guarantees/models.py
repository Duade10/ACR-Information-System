from core.models import AbstractTimeStampedModel
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from notifications import models as notifications_models


class ProtectionGuarantee(AbstractTimeStampedModel):
    """Protection Guarantee Of1 Model Definition"""

    STATION_GUARANTEE = "s.g"
    WORK_AND_TEST_PERMIT = "w&t.p"
    WORK_PERMIT = "w.t"

    FOR_A_CHOICES = (
        (STATION_GUARANTEE, "S.G"),
        (WORK_AND_TEST_PERMIT, "W&T.P"),
        (WORK_PERMIT, "W.T"),
    )

    applied_to_132 = models.ForeignKey(
        "stations_132.Station_132",
        related_name="protection_guarantees",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    applied_to_132_330 = models.ForeignKey(
        "stations_330.Station_330",
        related_name="protection_guarantees_132_330",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    applied_to_330 = models.ForeignKey(
        "stations_330.Station_330",
        related_name="protection_guarantees",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    for_a = models.CharField(choices=FOR_A_CHOICES, max_length=6)
    to_be_issued = models.DateField()
    to_be_issued_to = models.CharField(max_length=25)
    title = models.CharField(max_length=10)
    department = models.CharField(max_length=25)
    to_be_issued_at = models.DateTimeField()
    to_be_surrendered_at = models.DateTimeField()
    description_of_apparatus = models.TextField()
    additional_apparatus = models.TextField(null=True, blank=True)
    advance_request = models.ForeignKey(
        "users.User",
        related_name="protection_guarantees_advance_request",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    advance_request_name = models.CharField(max_length=30, null=True, blank=True)
    signature_of_applicant = models.CharField(max_length=50, null=True, blank=True)
    received_by = models.ForeignKey(
        "users.User",
        related_name="protection_guarantees_received",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    received_by_name = models.CharField(max_length=50, null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    outage = models.IntegerField()
    working_time = models.DurationField(null=True, blank=True)
    switching_time = models.DateTimeField(null=True, blank=True)
    apparatus_outage = models.CharField(max_length=50, null=True, blank=True)
    apparatus_outage_to = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        "users.User",
        related_name="protection_guarantees_approved",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approved_by_name = models.CharField(max_length=50, null=True, blank=True)
    approved_to = models.DateTimeField(null=True, blank=True)
    final_approval = models.ForeignKey(
        "users.User",
        related_name="protection_guarantees_final_approved",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    final_approval_name = models.CharField(max_length=50, null=True, blank=True)
    final_approval_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        "users.User",
        related_name="protection_guarantees",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user_name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    is_acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.for_a} - {self.pk}"

    def get_delete_url(self):
        return reverse("protection_guarantee:delete", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("protection_guarantees:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.designation == "132":
                self.slug = slugify(f"{self.user} - {self.pk} - {self.applied_to_132} - {self.for_a}")
                self.applied_to_132 = self.user.station_132
                self.applied_to_132_330 = self.user.station_132.station_330
            elif self.user.designation == "330":
                self.slug = slugify(f"{self.user} - {self.pk} - {self.applied_to_330} - {self.for_a}")
                self.applied_to_330 = self.user.station_330

            self.user_name = self.user.get_full_name()
            self.advance_request = self.user
            self.advance_request_name = self.user.get_full_name()

        self.working_time = self.to_be_surrendered_at - self.to_be_issued_at

        if self.received_by:
            self.received_by_name = self.received_by.get_full_name()

        super().save(*args, **kwargs)

    def created_notification(self, edit=False, station_330=None, station_132=None):
        user = self.user
        text = "sent an"
        if edit is True:
            text = "made changes to an"
        if user.designation == "132":
            station_132 = user.station_132
            to_station = station_132.station_330
            station = station_132
        elif user.designation == "330":
            station_330 = user.station_330
            to_station = user.station_330
            station = station_330
        text = f"{user.get_full_name()} ({station}) has {text} Application For Protection Guarantee (OF1)."
        notification = notifications_models.Notification.objects.create(
            from_user=user,
            from_station_330=station_330,
            from_station_132=station_132,
            text=text,
            icon="bell",
            url="/reports/protection-guarantees/",
        )
        notification.save()
        notification.to_station_330.add(to_station)
        return to_station.pk

    def edited_notification(self):
        self.created_notification(edit=True)
