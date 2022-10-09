from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, View
from stations_132 import models as stations_132_models

from . import forms, models


class FeederListView(View):
    def get(self, request, slug, *args, **kwargs):
        single_132station = get_object_or_404(stations_132_models.Station_132, slug=slug)
        all_feeders = single_132station.feeders.all()
        context = {"single_132station": single_132station, "all_feeders": all_feeders}
        return render(request, "feeders/feeder_list.html", context)


class FeederDetailView(DetailView):
    model = models.Feeder
    context_object_name = "single_feeder"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.FeederForm(instance=self.get_object())
        return context
