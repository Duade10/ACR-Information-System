from django.urls import path

from . import views

app_name = "troublereports"


urlpatterns = [
    path("search/", views.Search.as_view(), name="search"),
    path("", views.TroubleReportsListView.as_view(), name="list"),
    path("create/", views.TroublereportCreateView.as_view(), name="create"),
    path("edit/<int:pk>", views.TroublereportUpdateView.as_view(), name="edit"),
    path("acknowledge/<int:pk>/", views.Acknowledge.as_view(), name="acknowledge"),
    path("detail/<int:pk>", views.TroublereportsDetailView.as_view(), name="detail"),
]
