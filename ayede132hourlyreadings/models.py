import stations_132.models as stations_132_models
from ayede330hourlyreadings.models import AbstractHourlyReadingModel, Ayede330ReadingSheet
from core.models import AbstractTimeStampedModel
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from sheets.models import AbstractSheetModel
from sheets.google_sheet import GoogleSheet

# Daily Data Mail Imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class MaximumReadingError(Exception):
    """This error class is raised when a Hourly Reading Sheet has 24 Hourly Readings"""

    pass


class Ayede132GoogleSheetRange(AbstractTimeStampedModel):
    """Ayede 132 Hourly Reading Transformers And Total Load Google Sheet Range Database Model Definition"""

    name = models.CharField(max_length=40, null=True, blank=True)
    sheet_range = models.CharField(max_length=10, null=True, blank=True)
    station = models.ForeignKey("stations_132.station_132", default=2, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ayede 132 Google Sheet Range"
        verbose_name_plural = "Ayede 132 Google Sheet Range"

    def save(self, *args, **kwargs):
        self.name = str.upper(self.name)
        return super().save(args, kwargs)

    def __str__(self):
        return self.name


class Ayede132GoogleSheets(AbstractSheetModel):
    station = models.ForeignKey(
        "stations_132.station_132",
        related_name="station_google_sheets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    station_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.google_sheet_title} : {self.google_sheet_id}"

    class Meta:
        verbose_name = "Ayede 132 Google Sheet"
        verbose_name_plural = "Ayede 132 Google Sheets"

    def save(self, *args, **kwargs):
        self.station = stations_132_models.Station_132.objects.get(pk=2)
        self.station_name = f"{self.station.name}"
        self.google_sheet_title = str.upper(self.google_sheet_title)
        super().save(*args, **kwargs)


class Ayede132ReadingSheet(AbstractTimeStampedModel):
    created_at = models.DateTimeField()

    def get_daily_data(self):
        readings = self.hourly_readings.all()
        max_total_mw = max(readings.values_list("total_load_mw", flat=True))
        min_total_mw = min(readings.values_list("total_load_mw", flat=True))
        max_t1_mw = max(readings.values_list("t1_mw", flat=True))
        min_t1_mw = min(readings.values_list("t1_mw", flat=True))
        max_t2_mw = max(readings.values_list("t2_mw", flat=True))
        min_t2_mw = min(readings.values_list("t2_mw", flat=True))
        max_t3_mw = max(readings.values_list("t3_mw", flat=True))
        min_t3_mw = min(readings.values_list("t3_mw", flat=True))
        max_oluyole = max(readings.values_list("oluyole", flat=True))
        max_express = max(readings.values_list("express", flat=True))
        max_liberty = max(readings.values_list("liberty", flat=True))
        max_industrial = max(readings.values_list("industrial", flat=True))
        max_interchange = max(readings.values_list("interchange", flat=True))
        max_iyaganku = max(readings.values_list("iyaganku", flat=True))
        max_apata = max(readings.values_list("apata", flat=True))
        max_eleyele = max(readings.values_list("eleyele", flat=True))
        max_lanlate = max(readings.values_list("lanlate", flat=True))
        max_spare = max(readings.values_list("spare", flat=True))

        for i in readings:
            if i.total_load_mw == max_total_mw:
                max_station_total_mw_fq = i.frequency
                max_station_total_mw_hour = i.hour

            if i.total_load_mw == min_total_mw:
                min_station_total_mw_fq = i.frequency
                min_station_total_mw_hour = i.hour

            if i.t1_mw == max_t1_mw:
                max_t1_mw_fq = i.frequency
                max_t1_mw_hour = i.hour

            if i.t1_mw == min_t1_mw:
                min_t1_mw_fq = i.frequency
                min_t1_mw_hour = i.hour

            if i.t2_mw == max_t2_mw:
                max_t2_mw_fq = i.frequency
                max_t2_mw_hour = i.hour

            if i.t2_mw == min_t2_mw:
                min_t2_mw_fq = i.frequency
                min_t2_mw_hour = i.hour

            if i.t3_mw == max_t3_mw:
                max_t3_mw_fq = i.frequency
                max_t3_mw_hour = i.hour

            if i.t3_mw == min_t3_mw:
                min_t3_mw_fq = i.frequency
                min_t3_mw_hour = i.hour

            if i.oluyole == max_oluyole:
                max_oluyole_hour = i.hour

            if i.express == max_express:
                max_express_hour = i.hour

            if i.liberty == max_liberty:
                max_liberty_hour = i.hour

            if i.industrial == max_industrial:
                max_industrial_hour = i.hour

            if i.interchange == max_interchange:
                max_interchange_hour = i.hour

            if i.iyaganku == max_iyaganku:
                max_iyaganku_hour = i.hour

            if i.apata == max_apata:
                max_apata_hour = i.hour

            if i.eleyele == max_eleyele:
                max_eleyele_hour = i.hour

            if i.lanlate == max_lanlate:
                max_lanlate_hour = i.hour

            if i.spare == max_spare:
                max_spare_hour = i.hour

            daily_data = dict(
                max_total_mw=max_total_mw,
                max_station_total_mw_fq=max_station_total_mw_fq,
                max_station_total_mw_hour=max_station_total_mw_hour,
                min_total_mw=min_total_mw,
                min_station_total_mw_fq=min_station_total_mw_fq,
                min_station_total_mw_hour=min_station_total_mw_hour,
                max_t1_mw=max_t1_mw,
                max_t1_mw_fq=max_t1_mw_fq,
                max_t1_mw_hour=max_t1_mw_hour,
                min_t1_mw=min_t1_mw,
                min_t1_mw_fq=min_t1_mw_fq,
                min_t1_mw_hour=min_t1_mw_hour,
                max_t2_mw=max_t2_mw,
                max_t2_mw_fq=max_t2_mw_fq,
                max_t2_mw_hour=max_t2_mw_hour,
                min_t2_mw=min_t2_mw,
                min_t2_mw_fq=min_t2_mw_fq,
                min_t2_mw_hour=min_t2_mw_hour,
                max_t3_mw=max_t3_mw,
                max_t3_mw_fq=max_t3_mw_fq,
                max_t3_mw_hour=max_t3_mw_hour,
                min_t3_mw=min_t3_mw,
                min_t3_mw_fq=min_t3_mw_fq,
                min_t3_mw_hour=min_t3_mw_hour,
                max_oluyole=max_oluyole,
                max_oluyole_hour=max_oluyole_hour,
                max_express=max_express,
                max_express_hour=max_express_hour,
                max_liberty=max_liberty,
                max_liberty_hour=max_liberty_hour,
                max_industrial=max_industrial,
                max_industrial_hour=max_industrial_hour,
                max_interchange=max_interchange,
                max_interchange_hour=max_interchange_hour,
                max_iyaganku=max_iyaganku,
                max_iyaganku_hour=max_iyaganku_hour,
                max_apata=max_apata,
                max_apata_hour=max_apata_hour,
                max_eleyele=max_eleyele,
                max_eleyele_hour=max_eleyele_hour,
                max_lanlate=max_lanlate,
                max_lanlate_hour=max_lanlate_hour,
                max_spare=max_spare,
                max_spare_hour=max_spare_hour,
            )
            html_message = render_to_string("email/readings/ayede132_daily_data_email.html", daily_data)
            send_mail(
                f"Summary of relevant data ({self}",
                strip_tags(html_message),
                settings.EMAIL_HOST_USER,
                [
                    "otunlaisaac8@gmail.com",
                ],
                fail_silently=False,
                html_message=html_message,
            )

    def __str__(self):
        return f"Day: {self.created_at.day}, Month: {self.created_at.month}, Year: {self.created_at.year}"

    def get_absolute_url(self):
        return reverse("ayede132hourlyreadings:ayede_reading_sheet_hourly_readings", kwargs={"pk": self.pk})


class Ayede132HourlyReading(AbstractHourlyReadingModel):
    """Ayede 132 default hourly reading model"""

    hour = models.IntegerField()
    frequency = models.FloatField()

    iwo_iseyin_kv = models.FloatField()
    iwo_iseyin_a = models.FloatField()
    iwo_iseyin_mw = models.FloatField()
    iwo_iseyin_mvar = models.FloatField()

    jericho_kv = models.FloatField()
    jericho_a = models.FloatField()
    jericho_mw = models.FloatField()
    jericho_mvar = models.FloatField()

    mcpherson_kv = models.FloatField()
    mcpherson_a = models.FloatField()
    mcpherson_mw = models.FloatField()
    mcpherson_mvar = models.FloatField()

    t1_kv = models.FloatField()
    t1_a = models.FloatField(null=True, blank=True)
    t1_mw = models.FloatField(null=True, blank=True)
    t1_mvar = models.FloatField(null=True, blank=True)

    t2_kv = models.FloatField()
    t2_a = models.FloatField(null=True, blank=True)
    t2_mw = models.FloatField(null=True, blank=True)
    t2_mvar = models.FloatField(null=True, blank=True)

    t3_kv = models.FloatField()
    t3_a = models.FloatField(null=True, blank=True)
    t3_mw = models.FloatField(null=True, blank=True)
    t3_mvar = models.FloatField(null=True, blank=True)

    total_load_mw = models.FloatField(null=True, blank=True)
    total_load_mvar = models.FloatField(null=True, blank=True)

    oluyole = models.FloatField()
    express = models.FloatField()
    liberty = models.FloatField()
    industrial = models.FloatField()
    interchange = models.FloatField()
    iyaganku = models.FloatField()
    apata = models.FloatField()
    eleyele = models.FloatField()
    lanlate = models.FloatField()
    spare = models.FloatField(blank=True, null=True)

    is_uploaded = models.BooleanField(default=False)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField(max_length=40, null=True, blank=True)
    station = models.ForeignKey(
        "stations_132.Station_132",
        related_name="hourly_readings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reading_sheet = models.ForeignKey(
        Ayede132ReadingSheet,
        related_name="hourly_readings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.hour == 0:
            self.hour = 2400

        self.user_name = self.user.get_full_name()

        # DEFAULT 132KV STATION WITH PK(2) IS AYEDE 132 KV TS
        self.station = stations_132_models.Station_132.objects.get(pk=2)
        # T1
        self.t1_a = self.oluyole + self.express
        self.t1_mw = self.t1_a / 20
        self.t1_mvar = self.t1_mw / 2

        # T2
        self.t2_a = self.liberty + self.industrial + self.interchange + self.iyaganku
        self.t2_mw = self.t2_a / 20
        self.t2_mvar = self.t2_mw / 2

        # T2
        self.t3_a = self.apata + self.eleyele + self.lanlate
        self.t3_mw = self.t3_a / 20
        self.t3_mvar = self.t3_mw / 2

        # Total Load
        self.total_load_mw = int(self.t1_mw + self.t2_mw + self.t3_mw)
        self.total_load_mvar = int(self.t1_mvar + self.t2_mvar + self.t3_mvar)

        try:
            if self.created:
                obj = Ayede132ReadingSheet.objects.get(
                    Q(created_at__day=self.created.day)
                    & Q(created_at__month=self.created.month)
                    & Q(created_at__year=self.created.year)
                )
                if obj.hourly_readings.all().count() < 24:
                    self.reading_sheet = obj
                else:
                    raise Exception
            else:
                obj = Ayede132ReadingSheet.objects.get(
                    Q(created_at__day=timezone.now().day)
                    & Q(created_at__month=timezone.now().month)
                    & Q(created_at__year=timezone.now().year)
                )
                if obj.hourly_readings.all().count() < 24:
                    self.reading_sheet = obj
                else:
                    raise Exception

        except Exception:
            if self.created:
                obj = Ayede330ReadingSheet.objects.last()
                if obj.hourly_readings.all().count() < 24:
                    self.reading_sheet = obj
                x = Ayede132ReadingSheet.objects.create(created_at=self.created)
            else:
                x = Ayede132ReadingSheet.objects.create(created_at=timezone.now())
            self.reading_sheet = x

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hour {self.hour} - Total Load {self.total_load_mw}"

    def get_absolute_url(self):
        return reverse("ayede132hourlyreadings:list")

    def get_delete_url(self):
        return reverse("ayede132hourlyreadings:delete", kwargs={"pk": self.pk})

    def upload_reading(self, upload=True, clear=False):
        """
        Upload Ayede 132 Calculated hourly reading to various Google Sheets
        """
        # ACC STATION LOAD
        # sheet = Ayede132GoogleSheets.objects.get(pk=1)
        self.is_uploaded = True
        self.save()

    def clear_reading(self):
        """
        Remove Ayede 132 Calculated hourly reading from various Google Sheets
        """
        # ACC STATION LOAD
        # sheet = Ayede132GoogleSheets.objects.get(pk=1)
        self.upload_reading(upload=False, clear=True)
        self.is_uploaded = False
        self.save()
