from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class Station132UsersOnlyView(UserPassesTestMixin):
    """Allows only users with 132 designation"""

    def test_func(self):
        return self.request.user.designation == "132"

    def handle_no_permission(self):
        messages.error(self.request, "Permission reserved for 132kV Operators only")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)
