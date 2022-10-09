from django.urls import path

from . import views

app_name = "stations_330"

urlpatterns = [
    path("", views.Station330ListView.as_view(), name="list"),
    path("users/<int:pk>/", views.Station330UserListView.as_view(), name="users"),
    path("detail/<str:slug>", views.Station330DetailView.as_view(), name="detail"),
]
