from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("mark-all-as-read/", views.mark_all_as_read, name="mark_all_as_read"),
    path("<int:notification_pk>/", views.set_notification_as_seen, name="set_as_seen"),
]
