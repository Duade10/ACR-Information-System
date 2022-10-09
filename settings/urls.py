from django.urls import path

from . import views

app_name = "settings"

urlpatterns = [
    path("", views.settings, name="settings"),
    path("email-settings", views.EmailSettings.as_view(), name="email"),
    path("email-update", views.EmailFormUpdate.as_view(), name="email_update"),
    path("google-sheet-update/", views.GoogleSheetUpdate.as_view(), name="google_sheet_update"),
    path("google-sheet-settings/", views.GoogleSheetSetting.as_view(), name="google_sheet_setting"),
]
