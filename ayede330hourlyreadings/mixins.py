from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class Ayede330UserOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.designation == "330" and self.request.user.station_330.pk == 1

    def handle_no_permission(self):
        messages.error(self.request, "Permission Denied!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)
