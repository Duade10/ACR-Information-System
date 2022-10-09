import core.views as core_views
import users.mixins as users_mixins
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, UpdateView, View
from notifications import models as notifications_models
from stations_132 import models as stations_132_models
from stations_330 import mixins as station_330s_mixins
from stations_330 import models as stations_330_models

from . import forms, models


class TroublereportCreateView(users_mixins.LoggedInOnlyView, CreateView):
    model = models.TroubleReport
    form_class = forms.TroublereportForm
    template_name = "reports/troublereports/trouble_report_create.html"

    def form_valid(self, form):
        data = form.save()
        data.user = self.request.user
        data.save()
        core_views.socket_message(self.request, data.created_notification(), "troubleReports")
        return redirect("troublereports:list")


class TroublereportUpdateView(users_mixins.LoggedInOnlyView, UpdateView):
    model = models.TroubleReport
    form_class = forms.TroublereportForm
    template_name = "reports/troublereports/trouble_report_edit.html"

    def form_valid(self, form):
        data = form.save()
        data.save()
        core_views.socket_message(self.request, data.edited_notification(), "troubleReports")
        return redirect("troublereports:list")


class TroubleReportsListView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.designation == "330":
            single_station = get_object_or_404(stations_330_models.Station_330, pk=user.station_330.pk)
            trouble_reports = models.TroubleReport.objects.filter(
                Q(station_or_line_station_330=single_station) | Q(station_or_line_station_132_330=single_station)
            ).order_by("-created")
        if user.designation == "132":
            single_station = get_object_or_404(stations_132_models.Station_132, pk=user.station_132.pk)
            trouble_reports = models.TroubleReport.objects.filter(station_or_line_station_132=single_station).order_by(
                "-created"
            )
        paginator = Paginator(trouble_reports, 20)
        page = request.GET.get("page")
        trouble_reports = paginator.get_page(page)
        context = {
            "reports": trouble_reports,
            "single_station": single_station,
        }
        return render(request, "reports/troublereports/trouble_report_list.html", context)


class Search(users_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        user = request.user
        if "keyword" not in request.GET:
            return redirect(url)
        keyword = request.GET.get("keyword", None)
        user = request.user
        if user.designation == "330":
            single_station = get_object_or_404(stations_330_models.Station_330, pk=user.station_330.pk)
            trouble_reports = (
                models.TroubleReport.objects.filter(
                    Q(station_or_line_station_330=single_station) | Q(station_or_line_station_132_330=single_station)
                )
                .filter(
                    Q(to_authority__icontains=keyword)
                    | Q(location_of_trouble__icontains=keyword)
                    | Q(department__icontains=keyword)
                    | Q(number__icontains=keyword)
                    | Q(apparatus_in_trouble__icontains=keyword)
                    | Q(description_of_trouble__icontains=keyword)
                    | Q(description_of_switching__icontains=keyword)
                    | Q(user__first_name__icontains=keyword)
                    | Q(user__last_name__icontains=keyword)
                )
                .order_by("-created")
            )

        if user.designation == "132":
            single_station = get_object_or_404(stations_132_models.Station_132, pk=user.station_132.pk)
            trouble_reports = (
                models.TroubleReport.objects.filter(station_or_line_station_132=single_station)
                .filter(
                    Q(to_authority__icontains=keyword)
                    | Q(location_of_trouble__icontains=keyword)
                    | Q(department__icontains=keyword)
                    | Q(number__icontains=keyword)
                    | Q(apparatus_in_trouble__icontains=keyword)
                    | Q(description_of_trouble__icontains=keyword)
                    | Q(description_of_switching__icontains=keyword)
                    | Q(user__first_name__icontains=keyword)
                    | Q(user__last_name__icontains=keyword)
                )
                .order_by("-created")
            )
        paginator = Paginator(trouble_reports, 20)
        page = request.GET.get("page")
        trouble_reports = paginator.get_page(page)
        context = {
            "reports": trouble_reports,
            "single_station": single_station,
        }
        return render(request, "reports/troublereports/trouble_report_list.html", context)


class TroublereportsDetailView(users_mixins.LoggedInOnlyView, DetailView):
    model = models.TroubleReport
    context_object_name = "single_trouble_report"
    template_name = "reports/troublereports/trouble_report_detail.html"


class Acknowledge(users_mixins.LoggedInOnlyView, station_330s_mixins.Station330UsersOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        trouble_report = get_object_or_404(models.TroubleReport, pk=pk)
        trouble_report.acknowledged = True
        trouble_report.acknowledged_by = request.user
        trouble_report.save()
        user = request.user
        station = user.station_330
        notification = notifications_models.Notification.objects.create(
            from_user=user,
            from_station_330=station,
            icon="check",
            text=f"{user.get_full_name()} ({station}) has acknowleged your trouble report ({trouble_report.number})",
            url="/reports/trouble-reports/",
        )
        notification.save()
        if trouble_report.station_or_line_station_132 is not None:
            notification.to_station_132.add(trouble_report.station_or_line_station_132)
            to_station = trouble_report.station_or_line_station_132
        else:
            notification.to_station_330.add(trouble_report.station_or_line_station_330)
            to_station = trouble_report.station_or_line_station_330
        notification.save()
        core_views.socket_message(request, to_station.id, "troubleReports")
        messages.success(request, "Done!")
        return redirect(url)
