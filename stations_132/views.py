from django.views.generic import DetailView, View
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from stations_330 import models as stations_330_models
from . import models
import users.mixins as users_mixins
import random


class Station132ListView(View):
    def get(self, request, station330_pk, *args, **kwargs):
        station330 = get_object_or_404(stations_330_models.Station_330, pk=station330_pk)
        stations_132 = station330.stations_132.all()
        context = {"station330": station330, "stations_132": stations_132}
        return render(request, "stations_132/station_132_list.html", context)


class Station132DetailView(users_mixins.LoggedInOnlyView, DetailView):
    model = models.Station_132
    context_object_name = "single_station_132"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        of19_count = self.get_object().trouble_reports.count()
        users = self.get_object().users.order_by("?")[:5]
        context["users"] = users
        context["of19_count"] = of19_count
        return context


class Station132UserListView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        single_station = get_object_or_404(models.Station_132, pk=pk)
        users = single_station.users.all()
        paginator = Paginator(users, 20, orphans=5)
        page = request.GET.get("page")
        users = paginator.get_page(page)
        context = {"single_station_132": single_station, "users": users}
        return render(request, "stations_132/station_132_user_list.html", context)
