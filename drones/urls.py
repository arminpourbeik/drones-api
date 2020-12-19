from django.urls import path

from drones import views


urlpatterns = [
    path(
        "",
        views.ApiRoot.as_view(),
        name="ApiRoot",
    ),
    path(
        "drone-categories/",
        views.DroneCategoryList.as_view(),
        name="dronecategory-list",
    ),
    path(
        "drone-categories/<int:pk>",
        views.DroneCategoryDetail.as_view(),
        name="dronecategory-detail",
    ),
    path(
        "drones/",
        views.DroneList.as_view(),
        name="drone-list",
    ),
    path(
        "drones/<int:pk>",
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
