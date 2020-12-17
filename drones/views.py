from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from drones import models
from drones import serializers


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = models.DroneCategory.objects.all()
    serializer_class = serializers.DroneCategorySerializer


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DroneCategory.objects.all()
    serializer_class = serializers.DroneCategorySerializer


class DroneList(generics.ListCreateAPIView):
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer


class PilotList(generics.ListCreateAPIView):
    queryset = models.Pilot.objects.all()
    serializer_class = serializers.PilotSerializer


class PilotDetail(generics.ListCreateAPIView):
    queryset = models.Pilot.objects.all()
    serializer_class = serializers.PilotSerializer


class CompetitionList(generics.ListCreateAPIView):
    queryset = models.Competition.objects.all()
    serializer_class = serializers.PilotCompetitionSerializer


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Competition.objects.all()
    serializer_class = serializers.PilotCompetitionSerializer


class ApiRoot(generics.GenericAPIView):
    name = "Api Root"

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "drone-categories": reverse("dronecategory-list", request=request),
                "drones": reverse("drone-list", request=request),
                "pilots": reverse("pilot-list", request=request),
                "competitions": reverse("competition-list", request=request),
            }
        )
