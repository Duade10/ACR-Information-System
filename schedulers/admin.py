from django.contrib import admin
from . import models


@admin.register(models.ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    pass
