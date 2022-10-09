from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class Station330UsersOnlyView(UserPassesTestMixin):
    """Allows only users with 330 designation"""

    def test_func(self):
        return self.request.user.designation == "330"

    def handle_no_permission(self):
        messages.error(self.request, "Permission reserved for 330kV Operators only")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)
