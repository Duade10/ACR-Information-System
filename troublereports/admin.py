from django.contrib import admin
from . import models


@admin.register(models.TroubleReport)
class TroublereportAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "number",
        "station_or_line_station_132",
        "station_or_line_station_330",
        "acknowledged",
        "slug",
    )

    search_fields = ("user__first_name__icontains", "user__last_name__icontains")
