from core import custom_functions
from core import views as core_views
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from feeders import models as feeders_models
from notifications import models as notifications_models
from stations_132 import mixins as stations_132_mixins
from users import mixins as users_mixins

from . import models


class OperationalReportCreateView(users_mixins.LoggedInOnlyView, stations_132_mixins.Station132UsersOnlyView, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        frequency = None
        if request.POST.get("frequency") != "":
            frequency = request.POST.get("frequency")

        load_loss = None
        if request.POST.get("loadLoss") != "":
            load_loss = request.POST.get("loadLoss")

        operational_report = models.OperationalReport.objects.create(
            from_time=request.POST.get("fromTime", None),
            to_time=request.POST.get("toTime", None),
            feeder=feeders_models.Feeder.objects.get(pk=request.POST.get("feeder", None)),
            reason=request.POST.get("reason", None),
            frequency=frequency,
            description=request.POST.get("description", None),
            phase=request.POST.get("phase", None),
            load_loss=load_loss,
            user=request.user,
        )
        operational_report.save()
        station = user.station_132
        to_station = user.station_132.station_330
        text = f"{user.get_full_name()} ({station}) has sent an operational report."
        notification = notifications_models.Notification.objects.create(
            from_user=user,
            from_station_132=station,
            text=text,
            icon="bell",
            url="/reports/operational-reports/",
        )
        notification.save()
        notification.to_station_330.add(to_station)
        core_views.socket_message(request, to_station.id)
        response = {"msg": "Your form has been submitted successfully"}
        return JsonResponse(response)


class OperationalReportListView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        station = custom_functions.get_user_station(request.user)
        all_operational_report = station.operational_reports.all().order_by("-created")
        paginator = Paginator(all_operational_report, 5)
        page = request.GET.get("page")
        all_operational_reports = paginator.get_page(page)
        context = {
            "station": station,
            "reports": all_operational_reports,
        }
        return render(request, "reports/operational_reports/operational_report_list.html", context)


class OperationalReportMarkAsReadView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        try:
            report = get_object_or_404(models.OperationalReport, pk=pk)
            if report.is_read is True:
                report.is_read = False
            elif report.is_read is False:
                report.is_read = True
            report.save()
            return redirect(url)
        except Exception:
            return redirect("operational_reports:list")
