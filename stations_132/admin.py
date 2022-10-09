from django.contrib import admin
from . import models


@admin.register(models.Station_132)
class Station_132Admin(admin.ModelAdmin):
    def get_330kV_station(self, obj):
        return obj.station_330

    def count_feeders(self, obj):
        return obj.feeders.count()

    count_feeders.short_description = "Feeders"
    get_330kV_station.short_description = "330kV Station"
    list_display = ("__str__", "abbrevation", "count_feeders", "get_330kV_station")
