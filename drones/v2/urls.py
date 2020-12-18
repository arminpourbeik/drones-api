from django.urls import path

from drones import views
from drones.v2 import views as views_v2

app_name = "v2"

urlpatterns = [
    path(
        "",
        views_v2.ApiRootVersion2.as_view(),
        name="ApiRoot",
    ),
    path(
        "vehicle-categories/",
        views.DroneCategoryList.as_view(),
        name="dronecategory-list",
    ),
    path(
        "vehicle-categories/<int:pk>",
        views.DroneCategoryDetail.as_view(),
        name="dronecategory-detail",
    ),
    path(
        "vehicle/",
        views.DroneList.as_view(),
        name="drone-list",
    ),
    path(
        "vehicle/<int:pk>",
        views.DroneDetail.as_view(),
        name="drone-detail",
    ),
    path(
        "pilots/",
        views.PilotList.as_view(),
        name="pilot-list",
    ),
    path(
        "pilots/<int:pk>",
        views.PilotDetail.as_view(),
        name="pilot-detail",
    ),
    path(
        "competitions/",
        views.CompetitionList.as_view(),
        name="competition-list",
    ),
    path(
        "competitions/<int:pk>",
        views.CompetitionDetail.as_view(),
        name="competition-detail",
    ),
]