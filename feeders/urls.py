from django.urls import path
from . import views

app_name = "feeders"

urlpatterns = [
    path("<str:slug>/", views.FeederListView.as_view(), name="list"),
    path("detail/<str:pk>", views.FeederDetailView.as_view(), name="detail"),
]
