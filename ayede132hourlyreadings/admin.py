from django.contrib import admin

from . import models


@admin.register(models.Ayede132ReadingSheet)
class Ayede132ReadingSheet(admin.ModelAdmin):
    list_display = ("__str__", "count_hourly_reading")

    def count_hourly_reading(self, obj):
        return obj.hourly_readings.count()

    count_hourly_reading.short_description = "Hourly Reading"


@admin.register(models.Ayede132HourlyReading)
class Ayede132HourlyReadingAdmin(admin.ModelAdmin):
    list_display = (
        "hour",
        "frequency",
        "total_load_mw",
        "total_load_mvar",
        "user_name",
        "created",
    )


@admin.register(models.Ayede132GoogleSheets)
class Ayede132GoogleSheet(admin.ModelAdmin):
    list_display = ("__str__", "last_updated")

    def last_updated(self, obj):
        return obj.updated
