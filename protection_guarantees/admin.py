from django.contrib import admin

from . import models


@admin.register(models.ProtectionGuarantee)
class ProtectionGuaranteeAdmin(admin.ModelAdmin):
    list_display = ("user", "for_a", "created", "is_acknowledged")
    search_fields = ("user__first_name__icontains", "user__last_name__icontains")
