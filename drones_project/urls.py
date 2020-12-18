from django.contrib import admin
from django.urls import path, include


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api-auth/", include("rest_framework.urls")),
#     path("api/", include("drones.urls")),
# ]
urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/api/", include("drones.urls", namespace="v1")),
    path("v2/api/", include("drones.v2.urls", namespace="v2")),
    path("v1/api-auth/", include("rest_framework.urls")),
    path("v2/api-auth/", include("rest_framework.urls")),
]
