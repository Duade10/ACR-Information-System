from django.urls import path
from . import views

app_name = "operational_reports"

urlpatterns = [
    path("", views.OperationalReportListView.as_view(), name="list"),
    path("create/", views.OperationalReportCreateView.as_view(), name="create"),
    path("toggle-is-read/<int:pk>", views.OperationalReportMarkAsReadView.as_view(), name="is_read"),
]
