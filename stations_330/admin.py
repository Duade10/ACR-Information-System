from django.contrib import admin
from . import models


@admin.register(models.Station_330)
class Station_330Admin(admin.ModelAdmin):
    def count_132kv_stations(self, obj):
        return obj.stations_132.count()

    count_132kv_stations.short_description = "132kV Stations"
    list_display = ("__str__", "abbrevation", "count_132kv_stations")
