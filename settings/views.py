import core.views as core_views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from core.custom_functions import get_user_station
from users.mixins import LoggedInOnlyView, SupervisorOnlyView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import mixins


@login_required(login_url="core:login")
def settings(request):
    return render(request, "settings/settings.html")


class GoogleSheetSetting(LoggedInOnlyView, mixins.GoogleSheetStationOnlyView, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        if user.designation == "330":
            station = user.station_330
        if user.designation == "132":
            station = user.station_132
        return render(self.request, "settings/google_sheet_settings.html", context={"station": station})


class GoogleSheetUpdate(LoggedInOnlyView, mixins.GoogleSheetStationOnlyView, View):
    def post(self, *args, **kwargs):
        response = {"msg": "Update Failed"}
        sheet_pk = self.request.POST.get("sheetPk", None)
        sheetId = self.request.POST.get("sheetId", None)
        user = self.request.user
        if user.designation == "330":
            for google_sheet in user.station_330.station_google_sheets.all():
                if google_sheet.pk == int(sheet_pk):
                    google_sheet.google_sheet_id = sheetId
                    google_sheet.save()
                    core_views.socket_message(self.request, user.station_330.pk)
                    response = {"msg": f"{google_sheet.google_sheet_title} sheet id has been updated"}
        if user.designation == "132":
            for google_sheet in user.station_132.station_google_sheets.all():
                if google_sheet.pk == int(sheet_pk):
                    google_sheet.google_sheet_id = sheetId
                    google_sheet.save()
                    core_views.socket_message(self.request, user.station_132.pk)
                    response = {"msg": f"{google_sheet.google_sheet_title} sheet id has been updated"}
        return JsonResponse(response)


class EmailSettings(LoggedInOnlyView, SupervisorOnlyView, View):
    def get(self, request, *args, **kwargs):
        station = get_user_station(request.user)
        return render(request, "settings/email_settings.html", {"station": station})


class EmailFormUpdate(LoggedInOnlyView, SupervisorOnlyView, View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", None)
        if email is None or len(email) < 5:
            messages.warning(request, "Form is empty")
            return redirect("settings:email")
        else:
            station = get_user_station(request.user)
            station.email = email
            station.save()
            return redirect("settings:email")
