from django.urls import path
from . import views

app_name = "ayede132hourlyreadings"

urlpatterns = [
    path("", views.Ayede132HourlyReadingListView.as_view(), name="list"),
    path("create/", views.Ayede132HourlyReadingCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.Ayede132HourlyReadingUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.Ayede132HourlyReadingDeleteView.as_view(), name="delete"),
    path(
        "upload-multiple/",
        views.Ayede132HourlyUploadMultipleReadings.as_view(),
        name="upload_multiple",
    ),
    path("clear/<int:pk>", views.Ayede132HourlyReadingClearReading.as_view(), name="clear"),
    path("upload-single/", views.Ayede132HourlyUploadSingleReading.as_view(), name="upload_single"),
    path("ayede-reading-sheet/", views.Ayede132ReadingSheet.as_view(), name="reading_sheet"),
    path(
        "ayede-reading-sheet-hourly-reading/<int:pk>/",
        views.Ayede132ReadingSheetHourlyReadings.as_view(),
        name="ayede_reading_sheet_hourly_readings",
    ),
    path("daily-data/<int:pk>", views.Ayede132ReadingSheetDailyData.as_view(), name="get_daily_data"),
    path("export-as-csv/<int:pk>", views.Ayede132ExportCSV.as_view(), name="export_as_csv"),
]
