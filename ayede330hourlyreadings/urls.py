from django.urls import path

from . import views

app_name = "ayede330hourlyreadings"

urlpatterns = [
    path("", views.Ayede330HourlyReadingListView.as_view(), name="list"),
    path("create/", views.Ayede330HourlyReadingCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.Ayede330HourlyReadingUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.Ayede330HourlyReadingDeleteView.as_view(), name="delete"),
    path(
        "upload-multiple/",
        views.Ayede330HourlyUploadMultipleReadings.as_view(),
        name="upload_multiple",
    ),
    path("clear/", views.Ayede330HourlyReadingClearReading.as_view(), name="clear"),
    path("upload-single/", views.Ayede330HourlyUploadSingleReading.as_view(), name="upload_single"),
    path("ayede-reading-sheet/", views.Ayede330ReadingSheet.as_view(), name="reading_sheet"),
    path(
        "ayede-reading-sheet-hourly-reading/<int:pk>/",
        views.Ayede330ReadingSheetHourlyReadings.as_view(),
        name="ayede_reading_sheet_hourly_readings",
    ),
    path("export-as-csv/<int:pk>", views.Ayede330ExportCSV.as_view(), name="export_as_csv"),
    path("get-count/", views.get_count, name="get_count"),
    path("daily-data/<int:pk>", views.Ayede330ReadingSheetDailyData.as_view(), name="get_daily_data"),
]
