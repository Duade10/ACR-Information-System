import requests
from users import mixins as users_mixins
from operational_reports import forms as operational_reports_forms
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timesince, timezone
from django.views.generic import View
from schedulers.models import ScheduledReport
from sheets.google_sheet import GoogleSheet
from requests.exceptions import Timeout

from . import custom_functions


from asgiref.sync import async_to_sync


def socket_message(request, stationID=None, reload_type=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "broadcast", {"type": "establish_socket", "message": stationID, "reload_type": reload_type}
    )
    return HttpResponse("done")


@login_required(login_url="users:login")
def index(request):
    operational_report_form = operational_reports_forms.OperationalReportForm(request.user)
    try:
        station = custom_functions.get_user_station(request.user)
        reading = None
        if station.hourly_readings:
            reading = station.hourly_readings.last()
        trouble_reports = station.trouble_reports.all().order_by("-created")[0:3]
        protection_guarantees = station.protection_guarantees.all().order_by("-created")[0:3]
        context = {
            "station": station,
            "reading": reading.total_load_mw,
            "trouble_reports": trouble_reports,
            "protection_guarantees": protection_guarantees,
            "operational_report_form": operational_report_form,
        }
        return render(request, "core/index.html", context)
    except Exception:
        return render(request, "core/index.html", {"operational_report_form": operational_report_form})


@login_required(login_url="users:login")
def calender(request):
    return render(request, "core/calender.html")


class GetStationsLastLoad(users_mixins.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        station = custom_functions.get_user_station(request.user)
        sub_stations_list = []
        sub_stations_load = []
        try:
            requests.get("https://www.google.com", timeout=(3.05, 27))
            if request.user.designation == "132":
                station = custom_functions.get_user_station(request.user)
                sub_stations = station.station_330.stations_132.all()

            elif request.user.designation == "330":
                station = custom_functions.get_user_station(request.user)
                sub_stations = station.stations_132.all()

            for sub_station in sub_stations:
                gs = GoogleSheet(
                    station.station_google_sheets.get(pk=1).google_sheet_id,
                    f"{custom_functions.get_day(True)}!{sub_station.acc_station_load}",
                )
                try:
                    load = gs.read_sheet(last=True)
                    load = int(float(load.replace(" ' ", "")))
                except (SyntaxError, ValueError, AttributeError):
                    load = 0.0
                sub_stations_list.append(f"{sub_station.name}({load})")
                sub_stations_load.append(load)

            return JsonResponse(
                {
                    "success": True,
                    "sub_stations": sub_stations_list,
                    "sub_stations_load": sub_stations_load,
                }
            )
        except (Exception, Timeout):
            return JsonResponse({"success": False})


@login_required(login_url="users:login")
def reports(request):
    return render(request, "core/reports.html")


@login_required(login_url="users:login")
def get_readings_page(request, page):
    url = request.META.get("HTTP_REFERER")
    try:
        if request.user.designation == "330":
            if request.user.station_330.pk == 1:
                if page == "create":
                    return redirect("ayede330hourlyreadings:create")
                elif page == "list":
                    return redirect("ayede330hourlyreadings:list")
                elif page == "sheet":
                    return redirect("ayede330hourlyreadings:reading_sheet")
            else:
                return redirect("core:home")

        if request.user.designation == "132":
            if request.user.station_132.pk == 2:
                if page == "create":
                    return redirect("ayede132hourlyreadings:create")
                elif page == "list":
                    return redirect("ayede132hourlyreadings:list")
                elif page == "sheet":
                    return redirect("ayede132hourlyreadings:reading_sheet")
            else:
                return redirect("core:home")
    except Exception:
        return redirect(url)


@login_required(login_url="users:login")
def get_my_station(request):
    station = custom_functions.get_user_station(request.user)
    return redirect(station.get_absolute_url())


class GetHourlyReading(users_mixins.LoggedInOnlyView, View):
    """This View Gets The Last 5 Hourly Readings Station Load from each station with hourly reading"""

    def get(self, request, *args, **kwargs):
        try:
            station = custom_functions.get_user_station(request.user)
            reading_load = []
            reading_hour = []
            if station.hourly_readings:
                reading = station.hourly_readings.all().order_by("-created")[:6]
                for r in reading:
                    reading_load.append(r.total_load_mw)
                    reading_hour.append(f"{r.hour} Hrs")

            return JsonResponse(
                {
                    "reading_load": reading_load[::-1],
                    "reading_hour": reading_hour[::-1],
                }
            )
        except Exception:
            pass
            return JsonResponse(None)


class GetDateTimeAndScheduledReports(users_mixins.LoggedInOnlyView, View):
    """
    This view get the current date and time while also get checking for any scheduled report e.g Applcation For Guarantee
    This view is called every 2 minute (120000 milliseconds)
    """

    def get(self, request, *args, **kwargs):
        scheduled_reports = ScheduledReport.objects.filter(
            Q(is_displayed=False)
            & Q(broadcast_on__day=timezone.now().day)
            & Q(broadcast_on__month=timezone.now().month)
            & Q(broadcast_on__year=timezone.now().year)
        )
        try:
            for report in scheduled_reports:
                x = timesince.timeuntil(report.protection_guarantee.to_be_issued_at)
                time_until_broadcast_on = int(x.removesuffix("minutes").removesuffix("hours").removesuffix("days"))
                if time_until_broadcast_on <= 15:
                    data = report.get_protection_guarantee_s_report()
                    report.is_displayed = True
                    report.save()
                    return JsonResponse({"pr_report": data})
        except Exception:
            pass
        return JsonResponse({"pr_report": dict(bool=False)})
