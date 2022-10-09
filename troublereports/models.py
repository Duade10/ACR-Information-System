from core import custom_functions
from core.models import AbstractTimeStampedModel
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from notifications import models as notifications_models


class TroubleReport(AbstractTimeStampedModel):
    """Trouble Report Of19 database model definition"""

    PMSO = "pm(so)"
    PMT = "pm(t)"

    AUTHORITY_CHOICES = (
        (PMSO, "PM(SO)"),
        (PMT, "PM(T)"),
    )

    ISO = "iso"
    TSP = "tsp"

    DEPARTMENT_CHOICES = (
        (ISO, "ISO"),
        (TSP, "TSP"),
    )

    created_at = models.DateTimeField()
    user_name = models.CharField(max_length=50, blank=True, null=True)
    acknowledged_by_name = models.CharField(max_length=50, blank=True, null=True)
    to_authority = models.CharField(max_length=20, choices=AUTHORITY_CHOICES)
    location_of_trouble = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES)
    number = models.CharField(max_length=50, null=True, blank=True)
    apparatus_in_trouble = models.TextField()
    description_of_trouble = models.TextField(blank=True, null=True)
    description_of_switching = models.TextField(blank=True, null=True)
    acknowledged = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)
    station_or_line_station_132 = models.ForeignKey(
        "stations_132.Station_132",
        related_name="trouble_reports",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    station_or_line_station_330 = models.ForeignKey(
        "stations_330.Station_330",
        related_name="trouble_reports",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    station_or_line_station_132_330 = models.ForeignKey(
        "stations_330.Station_330",
        related_name="trouble_reports_132_330",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        "users.User",
        related_name="trouble_reports",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    acknowledged_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.number} {self.user.get_full_name()}"

    def get_absolute_url(self):
        return reverse("troublereports:detail", kwargs={"pk": self.pk})

    def get_number(self):
        dept = str.upper(self.department)
        year = str(self.created_at.year)[2:]
        suffix = ""

        if self.user.designation == "330":
            abb = str.upper(self.user.station_330.abbrevation)
            number = f"{abb}{suffix}/{dept}/{year}"
            no = self.user.station_330.trouble_reports.filter(number__icontains=number).count()
            if no != 1:
                no += 1
        if self.user.designation == "132":
            if self.user.station_132.name == "Ayede":
                suffix = "/132"
            number = f"{abb}{suffix}/{dept}/{year}"
            abb = str.upper(self.user.station_132.abbrevation)
            no = self.user.station_132.trouble_reports.filter(number__icontains=number).count()
            if no != 1:
                no += 1
        number = f"{abb}{suffix}/{dept}/{year}/{no}"
        return number

    def save(self, *args, **kwargs):
        self.user_name = self.user.get_full_name()
        self.number = str(self.get_number())
        self.slug = slugify(f"{self.number} {self.pk}")
        if self.user.station_132:
            self.station_or_line_station_132 = self.user.station_132
            self.station_or_line_station_132_330 = self.user.station_132.station_330
        elif self.user.station_330:
            self.station_or_line_station_330 = self.user.station_330
        self.location_of_trouble = str.capitalize(custom_functions.get_object_or_str(self.location_of_trouble))
        self.location = str.capitalize(custom_functions.get_object_or_str(self.location))
        self.description_of_trouble = str.capitalize(custom_functions.get_object_or_str(self.description_of_trouble))
        self.description_of_switching = str.capitalize(
            custom_functions.get_object_or_str(self.description_of_switching)
        )
        super(TroubleReport, self).save(*args, **kwargs)

    def created_notification(self, edit=False, station_132=None, station_330=None):
        user = self.user
        if user.designation == "330":
            station_330 = user.station_330
            to_station = station_330
            station = station_330
        elif user.designation == "132":
            station_132 = user.station_132
            to_station = station_132.station_330
            station = station_132

        text = "filed"
        if edit is True:
            text = "made changes to"

        text = f"{user.get_full_name()} ({station}) has {text} a Trouble Report."
        notification = notifications_models.Notification.objects.create(
            from_user=user,
            from_station_330=station_330,
            from_station_132=station_132,
            text=text,
            icon="bell",
            url="/reports/trouble-reports/",
        )
        notification.save()
        notification.to_station_330.add(to_station)
        return to_station.pk

    def edited_notification(self):
        return self.created_notification(edit=True)
