from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("secret/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("users/", include("users.urls", namespace="users")),
    path("feeders/", include("feeders.urls", namespace="feeders")),
    path("stations-330/", include("stations_330.urls", namespace="stations_330")),
    path("stations-132/", include("stations_132.urls", namespace="stations_132")),
    path("notifications/", include("notifications.urls", namespace="notifications")),
    path("settings/", include("settings.urls", namespace="settings")),
    path(
        "reports/protection-guarantees/",
        include("protection_guarantees.urls", namespace="protection_guarantees"),
    ),
    path("reports/trouble-reports/", include("troublereports.urls", namespace="troublereports")),
    path(
        "reports/operational-reports/",
        include("operational_reports.urls", namespace="operational_reports"),
    ),
    path(
        "readings/ayede-330-hourly-reading/",
        include("ayede330hourlyreadings.urls", namespace="ayede330hourlyreadings"),
    ),
    path(
        "readings/ayede-132-hourly-reading/",
        include("ayede132hourlyreadings.urls", namespace="ayede132hourlyreadings"),
    ),
]


handler500 = "config.views.error_500"
handler404 = "config.views.error_404"
handler400 = "config.views.error_400"
handler503 = "config.views.error_503"


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
