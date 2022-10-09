from django.contrib import admin

from . import models


@admin.register(models.Ayede330GoogleSheetRange)
class Ayede330GoogleSheetRangeAdmin(admin.ModelAdmin):
    """Ayede 330 Hourly Readings Google Sheet Range Admin Panel Definition"""

    list_display = ("__str__", "sheet_range")

    pass


@admin.register(models.Ayede330ReadingSheet)
class Ayede330ReadingSheetAdmin(admin.ModelAdmin):
    """Ayede 330 Hourly Reading Sheet Admin Panel Definition"""

    list_display = ("__str__", "count_hourly_reading")

    def count_hourly_reading(self, obj):
        return obj.hourly_readings.count()

    count_hourly_reading.short_description = "Hourly Reading"


@admin.register(models.Ayede330HourlyReading)
class Ayede330HourlyReadingAdmin(admin.ModelAdmin):
    """Ayede 330 Hourly Reading Admin Panel Definition"""

    list_display = (
        "hour",
        "frequency",
        "total_load_a",
        "total_load_mw",
        "user_name",
        "created",
    )


@admin.register(models.Ayede330GoogleSheets)
class Ayede330GoogleSheet(admin.ModelAdmin):
    """Ayede 330 Hourly Reading Google Sheet Admin Panel Definition"""

    list_display = ("__str__", "last_updated")

    def last_updated(self, obj):
        return obj.updated
