from django.contrib import admin

from . import models


@admin.register(models.Feeder)
class FeederAdmin(admin.ModelAdmin):
    def get_132kV_station(self, obj):
        return obj.station_132

    def get_330kV_station(self, obj):
        return obj.station_132.station_330

    get_132kV_station.short_description = "132kV Station"
    get_330kV_station.short_description = "330kV Station"
    list_display = ("__str__", "get_132kV_station", "get_330kV_station")
