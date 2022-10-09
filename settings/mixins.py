from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class GoogleSheetStationOnlyView(UserPassesTestMixin):
    """View is only available to stations with Google Sheet App Configuration"""

    def test_func(self):
        try:
            if self.request.user.designation == "132":
                if len(self.request.user.station_132.station_google_sheets.all()) <= 0:
                    return False
                else:
                    return True
            elif self.request.user.designation == "330":
                if len(self.request.user.station_330.station_google_sheets.all()) <= 0:
                    return False
                else:
                    return True

            else:
                return False
        except AttributeError:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "No Google Sheet Setting available for your station!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)
