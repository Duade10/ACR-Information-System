from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Permission Denied!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)


class SupervisorOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.supervisor

    def handle_no_permission(self):
        messages.error(self.request, "Permission Denied!")
        try:
            url = self.request.META.get("HTTP_REFERER")
            return redirect(url)
        except TypeError:
            url = "core:home"
            return redirect(url)
