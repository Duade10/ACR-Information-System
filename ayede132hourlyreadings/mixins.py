from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class Ayede132UserOnlyView(UserPassesTestMixin):
    """Only allows users from Ayede 132 Station"""

    def test_func(self):
        return self.request.user.designation == "132" and self.request.user.station_132.pk == 2

    def handle_no_permission(self):
        messages.error(self.request, "Permission Denied!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)
