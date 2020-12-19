from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle

from django_filters import rest_framework as filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter

from drones import models
from drones import serializers
from drones import custompermissions


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = models.DroneCategory.objects.all()
    serializer_class = serializers.DroneCategorySerializer
    filterset_fields = ("name",)
    search_fields = ("^name",)
    ordering_fields = ("name",)


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DroneCategory.objects.all()
    serializer_class = serializers.DroneCategorySerializer


class DroneList(generics.ListCreateAPIView):
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer
    filterset_fields = (
        "name",
        "drone_category",
        "manufacturing_date",
        "has_it_competed",
    )
    search_fields = ("name",)
    ordering_fields = (
        "name",
        "manufacturing_date",
    )

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "drones"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermissions.IsCurrentUserOwnerOrReadOnly,
    )
    throttle_classes = (ScopedRateThrottle,)
    throtttle_scope = "drones"


class PilotList(generics.ListCreateAPIView):
    queryset = models.Pilot.objects.all()
    serializer_class = serializers.PilotSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = (
        "name",
        "gender",
        "races_count",
    )
    search_fields = ("^name",)
    ordering_fields = (
        "name",
        "races_count",
    )
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "pilots"


class PilotDetail(generics.ListCreateAPIView):
    queryset = models.Pilot.objects.all()
    serializer_class = serializers.PilotSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "pilots"


class CompetitionFilter(filters.FilterSet):
    from_achievment_date = DateTimeFilter(
        field_name="distance_achievment_date", lookup_expr="gte"
    )
    to_achievment_date = DateTimeFilter(
        field_name="distance_achievment_date", lookup_expr="lte"
    )
    min_distance_in_feet = NumberFilter(
        field_name="distance_in_feet", lookup_expr="gte"
    )
    max_distance_in_feet = NumberFilter(
        field_name="distance_in_feet", lookup_expr="lte"
    )
    drone_name = AllValuesFilter(field_name="drone__name")
    pilot_name = AllValuesFilter(field_name="pilot__name")

    class Meta:
        model = models.Competition
        fields = (
            "distance_in_feet",
            "from_achievment_date",
            "to_achievment_date",
            "min_distance_in_feet",
            "max_distance_in_feet",
            "drone_name",
            "pilot_name",
        )


class CompetitionList(generics.ListCreateAPIView):
    queryset = models.Competition.objects.all()
    serializer_class = serializers.PilotCompetitionSerializer
    filter_class = CompetitionFilter
    ordering_fields = (
        "distance_in_feet",
        "distance_achievment_date",
    )


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
