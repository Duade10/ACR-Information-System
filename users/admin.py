from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "gender",
        "is_staff",
        "is_superuser",
    )
    # list_filter = ("superhost", "language", "currency")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom User Fields",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "designation",
                    "station_330",
                    "station_132",
                    "supervisor",
                )
            },
        ),
    )

    search_fields = ("station_330__name__icontains", "station_132__name__icontains", "username__icontains")
