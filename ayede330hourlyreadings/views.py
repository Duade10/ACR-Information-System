import csv

import core.views as core_views
import requests
import users.mixins as users_mixins
from core import custom_functions
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from requests.exceptions import Timeout

from . import forms, mixins, models


class Ayede330HourlyReadingCreateView(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, CreateView):
    """View for creating a new Ayede 330 Hourly Reading, with a response rendered by a template."""

    model = models.Ayede330HourlyReading
    form_class = forms.Ayede330HourlyReadingForm
    template_name = "reading/ayede330hourlyreading/ayede330hourlyreading_create.html"

    def form_valid(self, form):
        url = self.request.META.get("HTTP_REFERER")
        hour = form.cleaned_data.get("hour")
        if forms.check_hour(hour) is False:
            messages.error(self.request, f"Hourly Reading with hour {hour} already exists")
            return redirect(url)
        else:
            data = form.save()
            data.user = self.request.user
            data.save()
            station = custom_functions.get_user_station(self.request.user)
            core_views.socket_message(self.request, station.id, "hourlyReading")
            messages.success(self.request, f"{data.hour} has been saved successfully")
            return super().form_valid(form)


class Ayede330HourlyReadingListView(users_mixins.LoggedInOnlyView, View):
    """
    Render a list of Ayede 330 Hourly Readings, set by a queryset of the hourly readings
    queried from the last Ayede 330 Reading Sheet created.
    """

    def get(self, request, *args, **kwargs):
        now = timezone.now() + timezone.timedelta(hours=1)
        last_reading_sheet = models.Ayede330ReadingSheet.objects.last()
        qs = last_reading_sheet.hourly_readings.all().order_by("-hour")
        paginator = Paginator(qs, 12, orphans=5)
        page = request.GET.get("page", 1)
        hourly_readings = paginator.get_page(page)
        return render(
            request,
            "reading/ayede330hourlyreading/ayede330hourlyreading_list.html",
            {"last_reading_sheet": last_reading_sheet, "hourly_readings": hourly_readings, "now": now},
        )


class Ayede330HourlyReadingDeleteView(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, View):
    """
    View for deleting a Ayede 330 Hourly Reading retrieved with the primary key.
    """

    def get(self, request, pk, *args, **kwargs):
        reading = models.Ayede330HourlyReading.objects.get(pk=pk)
        reading.clear_reading()
        url = reading.get_absolute_url()
        reading.delete()
        messages.success(request, "Hourly Reading Deleted!")
        return redirect(url)


class Ayede330HourlyReadingUpdateView(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, UpdateView):
    model = models.Ayede330HourlyReading
    form_class = forms.Ayede330HourlyReadingForm
    context_object_name = "single_reading"
    template_name = "reading/ayede330hourlyreading/ayede330hourlyreading_edit.html"

    def form_valid(self, form):
        data = form.save()
        data.save()
        station = custom_functions.get_user_station(data.user)
        core_views.socket_message(self.request, station.id, "hourlyReading")
        messages.success(
            self.request,
            f"Chances made successfully - Date: {data.created.date()} Hour: {data.hour} ",
        )
        return super().form_valid(form)


class Ayede330HourlyUploadSingleReading(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, View):
    def post(self, request, *args, **kwargs):
        response = {"msg": "Couldn't upload reading!"}
        reading_pk = request.POST.get("readingPk", None)
        reading = models.Ayede330HourlyReading.objects.get(pk=int(reading_pk))
        if not reading.is_uploaded:
            try:
                reading.upload_reading()
                response = {"msg": f"Hourly Reading {reading.hour} has been uploaded successfully..."}
            except Exception:
                pass
        else:
            response = {"msg": f"Hourly Reading {reading.hour} has already been uploaded..."}
            pass
        core_views.socket_message(request, request.user.station_330.id)
        return JsonResponse(response)


class Ayede330HourlyReadingClearReading(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, View):
    def post(self, request, *args, **kwargs):
        response = {"msg": "Couldn't clear reading!"}
        reading_pk = request.POST.get("readingPk", None)
        reading = models.Ayede330HourlyReading.objects.get(pk=int(reading_pk))

        if reading.is_uploaded:
            try:
                reading.clear_reading()
                response = {"msg": f"Hourly Reading {reading.hour} has been cleared succesfully..."}
            except Exception:
                pass
        else:
            response = {"msg": f"Hourly Reading {reading.hour} has already been clear..."}
            pass
        core_views.socket_message(request, request.user.station_330.id)
        return JsonResponse(response)


class Ayede330HourlyUploadMultipleReadings(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, View):
    def post(self, request, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        readings = request.POST.getlist("readings", None)
        command = request.POST.get("command", None)
        if command == "Choose..." and readings == []:
            messages.warning(request, "No field or hourly reading selected")
            return redirect(url)

        if command != "Choose..." and readings == []:
            messages.warning(request, "No hourly reading selected")
            return redirect(url)

        if command == "Choose..." and readings != []:
            messages.warning(request, "No field selected")
            return redirect(url)
        try:

            url = self.request.META.get("HTTP_REFERER")
            requests.get("https://www.google.com", timeout=(3.05, 27))
            readings = request.POST.getlist("readings")
            reading_hour = [int(models.Ayede330HourlyReading.objects.get(pk=pk).hour) for pk in readings]
            reading_hour.sort(key=None, reverse=True)
            for hour in reading_hour[::-1]:
                for reading in models.Ayede330ReadingSheet.objects.last().hourly_readings.all():
                    if hour == reading.hour:
                        if int(command) == 1:
                            if not reading.is_uploaded:
                                reading.upload_reading()
                                messages.success(
                                    request,
                                    f"Load: {reading.total_load_mw}, Hour: {reading.hour} has been uploaded",
                                )
        except (Exception, Timeout):
            messages.error(request, "Couldn't complete request")
            pass
        return redirect(url)


class Ayede330ReadingSheet(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, ListView):
    model = models.Ayede330ReadingSheet
    template_name = "reading/ayede330hourlyreading/sheet_list.html"
    context_object_name = "reading_sheets"
    paginate_by = 28
    paginate_orphans = 4
    ordering = "-created"


class Ayede330ReadingSheetHourlyReadings(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, DetailView):
    model = models.Ayede330ReadingSheet
    template_name = "reading/ayede330hourlyreading/sheet_readings.html"
    context_object_name = "single_reading_sheet"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        readings = self.get_object().hourly_readings.all()
        max_station_load = max(readings.values_list("total_load_mw", flat=True))
        min_station_load = min(readings.values_list("total_load_mw", flat=True))
        count = readings.count()
        context["count"] = count
        context["max_station_load"] = max_station_load
        context["min_station_load"] = min_station_load
        return context


class Ayede330ReadingSheetDailyData(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        reading_sheet = get_object_or_404(models.Ayede330ReadingSheet, pk=pk)
        try:
            requests.get("https://www.google.com", timeout=(3.05, 27))
            reading_sheet.get_daily_data()
            messages.success(request, "Request completed")
        except (Exception, Timeout):
            messages.error(request, "Couldn't complete request")
            pass
        return redirect(reading_sheet.get_absolute_url())


class Ayede330ExportCSV(users_mixins.LoggedInOnlyView, mixins.Ayede330UserOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        reading_sheet = get_object_or_404(models.Ayede330ReadingSheet, pk=pk)
        response["Content-Dispositon"] = f"attachment; filename:{reading_sheet}.csv"
        # Create  a CSV Writer
        writer = csv.writer(response)

        # Get Header
        writer.writerow(
            [
                "",
                "",
                "HOURLY READING SHEET",
                "",
                "",
                "",
                "",
                f"{reading_sheet}",
                "",
                "",
                "",
                "",
                "",
            ]
        )

        writer.writerow(
            [
                "",
                "Date",
                "Frequency",
                "Hour",
                "OSOGBO",
                "OLORUNSOGO",
                "T1A",
                "T2A",
                "T2B",
                "TOTAL LOAD",
                "SAGAMU",
                "JERICHO",
                "IBN/IWO/ISEYIN",
            ]
        )

        writer.writerow(
            [
                "",
                "DATE",
                "FREQUENCY",
                "HOUR",
                "KV | A | MW | MVAR",
                "KV | A | MW | MVAR",
                "KV | A | MW | MVAR",
                "KV | A | MW | MVAR",
                "KV | A | MW | MVAR",
                "A/MW",
                "KV | A | MW | MVAR",
                "KV | A | MW | MVAR",
                "KV | A | MW | MVAR",
            ]
        )
        for index, hr in enumerate(reading_sheet.hourly_readings.all()):
            writer.writerow(
                [
                    f"{index+1}",
                    f"{hr.created}",
                    f"{hr.frequency}",
                    f"{hr.oshogbo_kv} | {hr.oshogbo_a} | {hr.oshogbo_mw} | {hr.oshogbo_mvar}",
                    f"{hr.olorunsogo_kv} | {hr.olorunsogo_a} | {hr.olorunsogo_mw} | {hr.olorunsogo_mvar}",
                    f"{hr.t1a_kv} | {hr.t1a_a} | {hr.t1a_mw} | {hr.t1a_mvar}",
                    f"{hr.t2a_kv} | {hr.t2a_a} | {hr.t2a_mw} | {hr.t2a_mvar}",
                    f"{hr.t2b_kv} | {hr.t2b_a} | {hr.t2b_mw} | {hr.t2b_mvar}",
                    f"{hr.total_load_a} | {hr.total_load_mw}",
                    f"{hr.sagamu_kv} | {hr.sagamu_a} | {hr.sagamu_mw} | {hr.sagamu_mvar}",
                    f"{hr.jericho_kv} | {hr.jericho_a} | {hr.jericho_mw} | {hr.jericho_mvar}",
                    f"{hr.iwo_iseyin_kv} | {hr.iwo_iseyin_a} | {hr.iwo_iseyin_mw} | {hr.iwo_iseyin_mvar}",
                ]
            )
        return response


def get_count(request):
    models.Ayede330ReadingSheet.objects.get_count_or_none(created_at__day=5)
