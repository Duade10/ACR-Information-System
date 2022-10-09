from django.urls import path
from . import views

app_name = "stations_132"

urlpatterns = [
    path("<int:station330_pk>", views.Station132ListView.as_view(), name="list"),
    path("users/<int:pk>/", views.Station132UserListView.as_view(), name="users"),
    path("detail/<str:slug>", views.Station132DetailView.as_view(), name="detail"),
]
