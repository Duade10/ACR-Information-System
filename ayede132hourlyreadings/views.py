import core.views as core_views
import users.mixins as users_mixins
from core import custom_functions
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from . import forms, mixins, models


class Ayede132HourlyReadingCreateView(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, CreateView):
    model = models.Ayede132HourlyReading
    form_class = forms.Ayede132HourlyReadingForm
    template_name = "reading/ayede132hourlyreading/ayede132hourlyreading_create.html"

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
            core_views.socket_message(self.request, station.id)
            return super().form_valid(form)


class Ayede132HourlyReadingListView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        now = timezone.now() + timezone.timedelta(hours=1)
        single_reading_sheet = models.Ayede132ReadingSheet.objects.last()
        return render(
            request,
            "reading/ayede132hourlyreading/ayede132hourlyreading_list.html",
            {"single_reading_sheet": single_reading_sheet, "now": now},
        )


class Ayede132HourlyReadingUpdateView(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, UpdateView):
    model = models.Ayede132HourlyReading
    form_class = forms.Ayede132HourlyReadingForm
    context_object_name = "single_reading"
    template_name = "reading/ayede132hourlyreading/ayede132hourlyreading_edit.html"

    def form_valid(self, form):
        data = form.save()
        data.save()
        station = custom_functions.get_user_station(data.user)
        core_views.socket_message(self.request, station.id)
        messages.success(
            self.request,
            f"Chances made successfully - Date: {data.created.date()} Hour: {data.hour} ",
        )
        return super().form_valid(form)


class Ayede132HourlyReadingDeleteView(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        reading = models.Ayede132HourlyReading.objects.get(pk=pk)
        url = reading.get_absolute_url()
        reading.delete()
        return redirect(url)


class Ayede132HourlyUploadSingleReading(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, View):
    def post(self, request, *args, **kwargs):
        response = {"msg": "Couldn't upload reading!"}
        reading_pk = request.POST.get("readingPk", None)
        reading = models.Ayede132HourlyReading.objects.get(pk=int(reading_pk))
        if not reading.is_uploaded:
            try:
                reading.upload_reading()
                response = {"msg": f"Hourly Reading {reading.hour} has been uploaded successfully"}
            except Exception:
                pass
        else:
            response = {"msg": f"Hourly Reading {reading.hour} has already been uploaded successfully"}
            pass
        core_views.socket_message(request, request.user.station_132.id)
        return JsonResponse(response)


class Ayede132HourlyReadingClearReading(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        reading = models.Ayede132HourlyReading.objects.get(pk=pk)
        reading.clear_reading()
        messages.warning(
            request,
            f"Load {reading.total_load_mw}, Hour: {reading.hour} has been cleared succesfully",
        )
        return redirect(url)


class Ayede132HourlyUploadMultipleReadings(users_mixins.LoggedInOnlyView, View):
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

        url = self.request.META.get("HTTP_REFERER")
        readings = request.POST.getlist("readings")
        reading_hour = [int(models.Ayede132HourlyReading.objects.get(pk=pk).hour) for pk in readings]
        reading_hour.sort(key=None, reverse=True)
        for hour in reading_hour[::-1]:
            for reading in models.Ayede132ReadingSheet.objects.last().hourly_readings.all():
                if hour == reading.hour:
                    if int(command) == 1:
                        if not reading.is_uploaded:
                            reading.upload_reading()
                            messages.success(
                                request,
                                f"Load: {reading.total_load_mw}, Hour: {reading.hour} has been uploaded",
                            )
        return redirect(url)


class Ayede132ReadingSheet(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, ListView):
    model = models.Ayede132ReadingSheet
    template_name = "reading/ayede132hourlyreading/sheet_list.html"
    context_object_name = "reading_sheets"
    paginate_by = 10
    paginate_orphans = 4
    ordering = "-created"


class Ayede132ReadingSheetHourlyReadings(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, DetailView):
    model = models.Ayede132ReadingSheet
    template_name = "reading/ayede132hourlyreading/sheet_readings.html"
    context_object_name = "single_reading_sheet"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        readings = self.get_object().hourly_readings.all()
        max_station_load = max(readings.values_list("total_load_mw", flat=True))
        min_station_load = min(readings.values_list("total_load_mw", flat=True))
        context["max_station_load"] = max_station_load
        context["min_station_load"] = min_station_load
        context["count"] = readings.count()
        return context


class Ayede132ReadingSheetDailyData(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            reading_sheet = get_object_or_404(models.Ayede132ReadingSheet, pk=pk)
            reading_sheet.get_daily_data()
            messages.success(request, "Request completed")
        except Exception:
            messages.error(request, "Couldn't complete request")
            pass
        return redirect(reading_sheet.get_absolute_url())


class Ayede132ExportCSV(users_mixins.LoggedInOnlyView, mixins.Ayede132UserOnlyView, View):
    pass
