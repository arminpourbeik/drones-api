from django.contrib.auth.models import User
from rest_framework import serializers

from drones import models


class UserDroneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Drone
        fields = (
            "url",
            "name",
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "url",
            "pk",
            "username",
            "drones",
        )

    drones = UserDroneSerializer(many=True, read_only=True)


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="drone-detail",
    )

    class Meta:
        model = models.DroneCategory
        fields = (
            "url",
            "pk",
            "name",
            "drones",
        )


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    drone_category = serializers.SlugRelatedField(
        queryset=models.DroneCategory.objects.all(),
        slug_field="name",
    )
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = models.Drone
        fields = (
            "url",
            "name",
            "drone_category",
            "owner",
            "manufacturing_date",
            "has_it_competed",
            "inserted_timestamp",
        )


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    """Use to serialize competition instaces as the detail of a pilot"""

    drone = DroneSerializer()

    class Meta:
        model = models.Competition
        fields = (
            "url",
            "pk",
            "distance_in_feet",
            "distance_achievment_date",
            "drone",
        )


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=models.Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source="get_gender_display",
        read_only=True,
    )

    class Meta:
        model = models.Pilot
        fields = (
            "url",
            "name",
            "gender",
            "gender_description",
            "races_count",
            "inserted_timestamp",
            "competitions",
        )


class PilotCompetitionSerializer(serializers.ModelSerializer):
    """Use to serialize competition instance"""

    pilot = serializers.SlugRelatedField(
        queryset=models.Pilot.objects.all(), slug_field="name"
    )
    drone = serializers.SlugRelatedField(
        queryset=models.Drone.objects.all(), slug_field="name"
    )

    class Meta:
        model = models.Competition
        fields = (
            "url",
            "pk",
            "distance_in_feet",
            "distance_achievment_date",
            "pilot",
            "drone",
        )
