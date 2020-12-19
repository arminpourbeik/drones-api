from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from drones import views


class ApiRootVersion2(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "vehicle-categories": reverse("dronecategory-list", request=request),
                "vehicle": reverse("drone-list", request=request),
                "pilots": reverse("pilot-list", request=request),
                "competitions": reverse("competition-list", request=request),
            }
        )
