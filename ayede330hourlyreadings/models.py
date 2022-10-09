from email.policy import default
from core.models import AbstractTimeStampedModel
from django.conf import settings

# Account Verification Imports
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from sheets.google_sheet import GoogleSheet
from sheets.models import AbstractSheetModel
from stations_330 import models as stations_330_models


class MaximumReadingError(Exception):
    """This error class is raised when a Hourly Reading Sheet has 24 Hourly Readings"""

    pass


class Ayede330GoogleSheetRange(AbstractTimeStampedModel):
    """Ayede 330 Hourly Reading Transformers And Total Load Google Sheet Range Database Model Definition"""

    name = models.CharField(max_length=40, null=True, blank=True)
    sheet_range = models.CharField(max_length=10, null=True, blank=True)
    station = models.ForeignKey("stations_330.station_330", default=1, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ayede 330 Google Sheet Range"
        verbose_name_plural = "Ayede 330 Google Sheet Range"

    def save(self, *args, **kwargs):
        self.name = str.upper(self.name)
        return super().save(args, kwargs)

    def __str__(self):
        return self.name


class Ayede330GoogleSheets(AbstractSheetModel):
    station = models.ForeignKey(
        "stations_330.station_330",
        related_name="station_google_sheets",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    station_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Ayede 330 Google Sheet"
        verbose_name_plural = "Ayede 330 Google Sheets"

    def __str__(self):
        return f"{self.google_sheet_title} : {self.google_sheet_id}"

    def save(self, *args, **kwargs):
        self.station = stations_330_models.Station_330.objects.get(pk=1)
        self.station_name = f"{stations_330_models.Station_330.objects.get(pk=1)}"
        self.google_sheet_title = str.upper(self.google_sheet_title)
        super().save(*args, **kwargs)


class Ayede330ReadingSheet(AbstractTimeStampedModel):
    created_at = models.DateTimeField()

    class Meta:
        verbose_name = "Ayede 330 Reading Sheet"
        verbose_name_plural = "Ayede 330 Reading Sheets"

    def get_daily_data(self):
        readings = self.hourly_readings.all()
        first_hour = self.hourly_readings.first().hour
        first_created = self.hourly_readings.first().created
        last_hour = self.hourly_readings.last().hour
        last_created = self.hourly_readings.last().created
        max_total_load_mw = max(readings.values_list("total_load_mw", flat=True))
        min_total_load_mw = min(readings.values_list("total_load_mw", flat=True))
        max_oshogbo_kv = max(readings.values_list("oshogbo_kv", flat=True))
        max_olorunsogo_kv = max(readings.values_list("olorunsogo_kv", flat=True))
        min_oshogbo_kv = min(readings.values_list("oshogbo_kv", flat=True))
        min_olorunsogo_kv = min(readings.values_list("olorunsogo_kv", flat=True))

        max_t2a_kv = max(readings.values_list("t2a_kv", flat=True))
        min_t2a_kv = min(readings.values_list("t2a_kv", flat=True))
        max_t2a_mw = max(readings.values_list("t2a_mw", flat=True))
        min_t2a_mw = min(readings.values_list("t2a_mw", flat=True))
        max_t2b_kv = max(readings.values_list("t2b_kv", flat=True))
        min_t2b_kv = min(readings.values_list("t2b_kv", flat=True))
        max_t2b_mw = max(readings.values_list("t2b_mw", flat=True))
        min_t2b_mw = min(readings.values_list("t2b_mw", flat=True))

        for i in readings:
            if i.total_load_mw == max_total_load_mw:
                max_station_total_mw_fq = i.frequency
                max_station_total_mw_hour = i.hour

            if i.total_load_mw == min_total_load_mw:
                min_station_total_mw_fq = i.frequency
                min_station_total_mw_hour = i.hour

            if i.oshogbo_kv == max_oshogbo_kv:
                max_oshogbo_kv_hour = i.hour

            if i.olorunsogo_kv == max_olorunsogo_kv:
                max_olorunsogo_kv_hour = i.hour

            if i.oshogbo_kv == min_oshogbo_kv:
                min_oshogbo_kv_hour = i.hour

            if i.olorunsogo_kv == min_olorunsogo_kv:
                min_olorunsogo_kv_hour = i.hour

            if i.t2a_mw == max_t2a_mw:
                max_t2a_mw_hour = i.hour
                max_t2a_mw_fq = i.frequency

            if i.t2a_mw == min_t2a_mw:
                min_t2a_mw_hour = i.hour
                min_t2a_mw_fq = i.frequency

            if i.t2a_kv == max_t2a_kv:
                max_t2a_kv_hour = i.hour
                max_t2a_kv_fq = i.frequency

            if i.t2a_kv == min_t2a_kv:
                min_t2a_kv_hour = i.hour
                min_t2a_kv_fq = i.frequency

            if i.t2b_mw == max_t2b_mw:
                max_t2a_mw_hour = i.hour
                max_t2a_mw_fq = i.frequency

            if i.t2b_mw == min_t2b_mw:
                min_t2a_mw_hour = i.hour
                min_t2a_mw_fq = i.frequency

            if i.t2b_kv == max_t2b_kv:
                max_t2a_kv_hour = i.hour
                max_t2a_mw_fq = i.frequency

            if i.t2b_kv == min_t2b_kv:
                min_t2a_kv_hour = i.hour
                min_t2a_kv_fq = i.frequency

        max_station_kv = max_oshogbo_kv
        max_station_kv_hour = max_oshogbo_kv_hour
        if max_olorunsogo_kv >= max_station_kv:
            max_station_kv = max_olorunsogo_kv
            max_station_kv_hour = max_olorunsogo_kv_hour

        min_station_kv = min_oshogbo_kv
        min_station_kv_hour = min_oshogbo_kv_hour
        if min_olorunsogo_kv >= min_station_kv:
            min_station_kv = min_olorunsogo_kv
            min_station_kv_hour = min_olorunsogo_kv_hour

        # current_site = get_current_site(request)
        daily_data = dict(
            first_hour=first_hour,
            first_created=first_created,
            last_hour=last_hour,
            last_created=last_created,
            min_station_kv_hour=min_station_kv_hour,
            min_station_kv=min_station_kv,
            max_station_kv_hour=max_station_kv_hour,
            max_station_kv=max_station_kv,
            max_station_total_mw_hour=max_station_total_mw_hour,
            max_station_total_mw_fq=max_station_total_mw_fq,
            max_station_mw=max_total_load_mw,
            min_station_total_mw_hour=min_station_total_mw_hour,
            min_station_total_mw_fq=min_station_total_mw_fq,
            min_station_total_mw=min_total_load_mw,
            max_oshogbo_kv_hour=max_oshogbo_kv_hour,
            max_oshogbo_kv=max_oshogbo_kv,
            max_olorunsogo_kv_hour=max_olorunsogo_kv_hour,
            max_olorunsogo_kv=max_olorunsogo_kv,
            max_t2a_kv=max_t2a_kv,
            max_t2a_kv_fq=max_t2a_kv_fq,
            max_t2a_kv_hour=max_t2a_kv_hour,
            min_t2a_kv=min_t2a_kv,
            min_t2a_kv_fq=min_t2a_kv_fq,
            min_t2a_kv_hour=min_t2a_kv_hour,
            max_t2a_mw=max_t2a_mw,
            min_t2a_mw=min_t2a_mw,
            max_t2b_kv=max_t2b_kv,
            min_t2b_kv=min_t2b_kv,
            max_t2b_mw=max_t2b_mw,
            min_t2b_mw=min_t2b_mw,
            max_t2a_mw_hour=max_t2a_mw_hour,
            max_t2a_mw_fq=max_t2a_mw_fq,
            min_t2a_mw_hour=min_t2a_mw_hour,
            min_t2a_mw_fq=min_t2a_mw_fq,
        )

        html_message = render_to_string(
            "email/readings/ayede330_daily_data_email.html",
            daily_data,
        )
        send_mail(
            f"Summary of relevant data ({self})",
            strip_tags(html_message),
            settings.EMAIL_HOST_USER,
            [
                "ayedeareacontrol@gmail.com",
            ],
            fail_silently=False,
            html_message=html_message,
        )

    def __str__(self):
        return f"Day: {self.created_at.day}, Month: {self.created_at.month}, Year: {self.created_at.year}"

    def get_absolute_url(self):
        return reverse("ayede330hourlyreadings:ayede_reading_sheet_hourly_readings", kwargs={"pk": self.pk})


class AbstractHourlyReadingModel(AbstractTimeStampedModel):
    hour = models.IntegerField()
    frequency = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        abstract = True


class Ayede330HourlyReading(AbstractHourlyReadingModel):
    """Ayede 330 Station Hourly Reading Database Model"""

    oshogbo_kv = models.FloatField()
    oshogbo_a = models.FloatField()
    oshogbo_mw = models.FloatField()
    oshogbo_mvar = models.FloatField()

    olorunsogo_kv = models.FloatField()
    olorunsogo_a = models.FloatField()
    olorunsogo_mw = models.FloatField(blank=True, null=True)
    olorunsogo_mvar = models.FloatField(blank=True, null=True)

    t1a_kv = models.FloatField(blank=True, null=True)
    t1a_a = models.FloatField(blank=True, null=True)
    t1a_mw = models.FloatField(blank=True, null=True)
    t1a_mvar = models.FloatField(blank=True, null=True)

    t2a_kv = models.FloatField()
    t2a_a = models.FloatField()
    t2a_mw = models.FloatField(blank=True, null=True)
    t2a_mvar = models.FloatField(blank=True, null=True)

    t2b_kv = models.FloatField()
    t2b_a = models.FloatField()
    t2b_mw = models.FloatField()
    t2b_mvar = models.FloatField()

    sagamu_kv = models.FloatField()
    sagamu_a = models.FloatField()
    sagamu_mw = models.FloatField()
    sagamu_mvar = models.FloatField()

    jericho_kv = models.FloatField()
    jericho_a = models.FloatField()
    jericho_mw = models.FloatField()
    jericho_mvar = models.FloatField()

    iwo_iseyin_kv = models.FloatField()
    iwo_iseyin_a = models.FloatField()
    iwo_iseyin_mw = models.FloatField()
    iwo_iseyin_mvar = models.FloatField()

    total_load_a = models.IntegerField(blank=True, null=True)
    total_load_mw = models.IntegerField(blank=True, null=True)

    is_uploaded = models.BooleanField(default=False)
    daily_area_load = models.BooleanField(default=False)
    transformer_hourly_load = models.BooleanField(default=True)
    active_load_flow = models.BooleanField(default=False)
    acc_stations_load = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User", related_name="hourly_readings", on_delete=models.SET_NULL, null=True, blank=True
    )
    user_name = models.CharField(max_length=40, null=True, blank=True)
    station = models.ForeignKey(
        "stations_330.Station_330",
        related_name="hourly_readings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reading_sheet = models.ForeignKey(
        Ayede330ReadingSheet,
        related_name="hourly_readings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ayede 330 Hourly Reading"
        verbose_name_plural = "Ayede 330 Hourly Readings"

    def save(self, *args, **kwargs):
        if self.hour == 0:
            self.hour = 2400

        if self.user:
            self.user_name = self.user.get_full_name()

        self.olorunsogo_mw = 0
        if self.olorunsogo_a:
            self.olorunsogo_mw = self.olorunsogo_a / 2

        if self.user:
            self.user_name = self.user.get_full_name()

        self.t1a_mw = 0
        if self.t1a_mw:
            self.t1a_mw = self.t1a_a / 5

        self.total_load_mw = int(self.t2b_mw + self.t2a_mw)
        self.total_load_a = int(self.t2b_a + self.t2a_a)

        self.station = stations_330_models.Station_330.objects.get(pk=1)

        try:
            if self.created:
                obj = Ayede330ReadingSheet.objects.get(
                    Q(created_at__day=self.created.day)
                    & Q(created_at__month=self.created.month)
                    & Q(created_at__year=self.created.year)
                )
                if obj.hourly_readings.all().count() < 24:
                    self.reading_sheet = obj
                else:
                    raise Exception
            else:
                obj = Ayede330ReadingSheet.objects.get(
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
                x = Ayede330ReadingSheet.objects.create(created_at=self.created)
            else:
                x = Ayede330ReadingSheet.objects.create(created_at=timezone.now())
            self.reading_sheet = x

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hour {self.hour} - Total Load {self.total_load_mw}"

    def get_absolute_url(self):
        return reverse("ayede330hourlyreadings:list")

    def get_delete_url(self):
        return reverse("ayede330hourlyreadings:delete", kwargs={"pk": self.pk})

    def upload_reading(self, upload=True, clear=False):
        """
        Upload Ayede 330 Calculated hourly reading to various Google Sheet
        """
        # ACC STATION LOAD
        acc_station_load = Ayede330GoogleSheets.objects.get(pk=1)
        acc_station_load_range = Ayede330GoogleSheetRange.objects.get(pk=1)

        # 330 KV ACTIVE LOAD FLOW
        active_load_flow = Ayede330GoogleSheets.objects.get(pk=3)
        active_load_flow_range_h2a = Ayede330GoogleSheetRange.objects.get(pk=2)
        active_load_flow_range_r2a = Ayede330GoogleSheetRange.objects.get(pk=3)

        # DAILY AREA LOAD
        daily_area_load = Ayede330GoogleSheets.objects.get(pk=2)
        daily_area_load_range = Ayede330GoogleSheetRange.objects.get(pk=4)

        # XFORMER HOURLY LOAD
        xformer_hourly_load = Ayede330GoogleSheets.objects.get(pk=4)
        xformer_hourly_load_range_t2a = Ayede330GoogleSheetRange.objects.get(pk=5)
        xformer_hourly_load_range_t2b = Ayede330GoogleSheetRange.objects.get(pk=7)

        day = timezone.now().day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "TH"
        else:
            suffix = ["ST", "ND", "RD"][day % 10 - 1]

        if upload is True:
            try:
                gs = GoogleSheet(
                    acc_station_load.google_sheet_id, f"{day}{suffix}!{acc_station_load_range.sheet_range}"
                )
                gs.append_sheet_column(self.total_load_mw)
            except Exception:
                pass

            # 330 KV ACTIVE LOAD FLOW
            try:
                gs = GoogleSheet(active_load_flow.google_sheet_id, f"{day}!{active_load_flow_range_h2a.sheet_range}")
                gs.append_sheet_row(self.oshogbo_mw)
                gs = GoogleSheet(active_load_flow.google_sheet_id, f"{day}!{active_load_flow_range_r2a.sheet_range}")
                gs.append_sheet_row(self.olorunsogo_mw)
                self.active_load_flow = True
                self.save()
            except Exception:
                pass

            # DAILY AREA LOAD
            try:
                gs = GoogleSheet(daily_area_load.google_sheet_id, f"{day}!{daily_area_load_range.sheet_range}")
                gs.append_sheet_column(self.total_load_mw)
                self.daily_area_load = True
                self.save()
            except Exception:
                pass

            # TRANSFORMER HOURLY LOAD
            try:
                gs = GoogleSheet(
                    xformer_hourly_load.google_sheet_id, f"{day}{suffix}!{xformer_hourly_load_range_t2a.sheet_range}"
                )
                gs.append_sheet_column(self.t2a_mw)
                gs = GoogleSheet(
                    xformer_hourly_load.google_sheet_id, f"{day}{suffix}!{xformer_hourly_load_range_t2b.sheet_range}"
                )
                gs.append_sheet_column(self.t2b_mw)
                self.save()
            except Exception:
                pass
            self.is_uploaded = True
            self.save()

        if clear is True:
            # ACC STATION LOAD
            try:
                gs = GoogleSheet(
                    acc_station_load.google_sheet_id, f"{day}{suffix}!{acc_station_load_range.sheet_range}"
                )
                gs.remove_last_sheet_column()
                self.acc_stations_load = False
                self.save()
            except Exception:
                pass

            # ACTIVE LOAD FLOW
            try:
                gs = GoogleSheet(
                    active_load_flow.google_sheet_id, f"{day}{suffix}!{active_load_flow_range_h2a.sheet_range}"
                )
                gs.remove_last_sheet_row()

            except Exception:
                pass

            try:
                gs = GoogleSheet(
                    active_load_flow.google_sheet_id, f"{day}{suffix}!{active_load_flow_range_r2a.sheet_range}"
                )
                gs.remove_last_sheet_row()
                self.active_load_flow = False
                self.save()
            except Exception:
                pass

            # DAILY AREA LOAD FLOW
            try:
                gs = GoogleSheet(daily_area_load.google_sheet_id, f"{day}{suffix}!{daily_area_load_range.sheet_range}")
                gs.remove_last_sheet_column()
                self.active_load_flow = False
                self.save()
            except Exception:
                pass

            # TRANSFORMER HOURLY LOAD
            try:
                gs = GoogleSheet(
                    xformer_hourly_load.google_sheet_id, f"{day}{suffix}!{xformer_hourly_load_range_t2a.sheet_range}"
                )
                gs.remove_last_sheet_column()
                self.transformer_hourly_load = False
                self.save()
            except Exception:
                pass

            try:
                gs = GoogleSheet(
                    xformer_hourly_load.google_sheet_id, f"{day}{suffix}!{xformer_hourly_load_range_t2b.sheet_range}"
                )
                gs.remove_last_sheet_column()
                self.transformer_hourly_load = False
                self.save()
            except Exception:
                pass

    def clear_reading(self):
        """
        Remove Ayede 330 Calculated hourly reading from various Google Sheet
        """
        # ACC STATION LOAD
        self.upload_reading(upload=False, clear=True)
        self.is_uploaded = False
        self.save()
