from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="home"),
    path("reports/", views.reports, name="reports"),
    path("calender/", views.calender, name="calender"),
    path("my-station/", views.get_my_station, name="my_station"),
    path("get-hourly-reading/", views.GetHourlyReading.as_view(), name="get_hourly_reading"),
    path("get-readings-page/<str:page>/", views.get_readings_page, name="get_readings_page"),
    path("get-stations-last-load/", views.GetStationsLastLoad.as_view(), name="get_stations_last_load"),
    path(
        "get-date-time-and-scheduled-reports/",
        views.GetDateTimeAndScheduledReports.as_view(),
        name="get_date_time_and_scheduled_reports",
    ),
]
