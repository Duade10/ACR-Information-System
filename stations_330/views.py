import random

import users.mixins as users_mixins
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, View

from . import models


class Station330ListView(users_mixins.LoggedInOnlyView, ListView):
    model = models.Station_330
    context_object_name = "stations_330"


class Station330DetailView(users_mixins.LoggedInOnlyView, DetailView):
    model = models.Station_330
    context_object_name = "single_station_330"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        of19_count = self.get_object().trouble_reports.count()
        users = self.get_object().users.order_by("?")[:5]
        context["of19_count"] = of19_count
        context["users"] = users
        return context


class Station330UserListView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        single_station = get_object_or_404(models.Station_330, pk=pk)
        users = single_station.users.all()
        paginator = Paginator(users, 20, orphans=5)
        page = request.GET.get("page")
        users = paginator.get_page(page)
        context = {"single_station_330": single_station, "users": users}
        return render(request, "stations_330/station_330_user_list.html", context)
