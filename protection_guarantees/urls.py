from django.urls import path

from . import views

app_name = "protection_guarantees"

urlpatterns = [
    path("", views.ProtetionGuaranteeListView.as_view(), name="list"),
    path("search/", views.Search.as_view(), name="search_protection_guarantee"),
    path("create/", views.ProtectionGuaranteeCreateView.as_view(), name="create"),
    path("acknowledge/<str:pk>/", views.Acknowledge.as_view(), name="acknowledge"),
    path("edit/<str:pk>/", views.ProtectionGuaranteeUpdateView.as_view(), name="update"),
    path("delete/<str:pk>/", views.ProtectionGuaranteeDeleteView.as_view(), name="delete"),
    path("detail/<str:pk>/", views.ProtectionGuaranteeDetailView.as_view(), name="detail"),
]
