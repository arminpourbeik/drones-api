from django.utils.http import urlencode
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import response, status
from rest_framework.settings import perform_import
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from drones.models import DroneCategory, Pilot
from drones import views


class DroneCategoryTests(APITestCase):
    def post_drone_category(self, name):
        url = reverse("dronecategory-list")
        data = {"name": name}
        response = self.client.post(url, data, format="json")
        return response

    def test_post_and_get_drone_category(self):
        """
        Ensure we can create a new Drone Category and then retrive it
        """

        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        print("PK {0}".format(DroneCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category(self):
        """
        Ensure we cannot create a new Drone Category with an existing name
        """

        url = reverse("dronecategory-list")
        new_drone_category_name = "Duplicated Copter"
        data = {"name": new_drone_category_name}
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_drone_category_by_name(self):
        """
        Ensure we can filter a drone category by name
        """

        drone_category_name1 = "Hexacopter"
        self.post_drone_category(drone_category_name1)
        drone_caregory_name2 = "Octocopter"
        self.post_drone_category(drone_caregory_name2)
        filter_by_name = {"name": drone_category_name1}
        url = "{0}?{1}".format(reverse("dronecategory-list"), urlencode(filter_by_name))
        print(url)
        response = self.client.get(url, format="json")
        print(response)

        assert response.status_code == status.HTTP_200_OK
        # Make sure we recieve only one element in the response
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == drone_category_name1

    def test_drone_categories_collection(self):
        """
        Ensure we can retrieve the drone categories collection
        """

        new_drone_category_name = "Super Copter"
        self.post_drone_category(new_drone_category_name)
        url = reverse("dronecategory-list")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        # Make sure we can receieve only one element in the response
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == new_drone_category_name

    def test_update_drone_category(self):
        """
        Ensure we can update a single field for a drone category
        """

        drone_category_name = "Categoty initial name"
        response = self.post_drone_category(drone_category_name)
        url = reverse("dronecategory-detail", None, {response.data.get("pk")})
        print(url)
        updated_drone_category_name = "Updated Name"
        data = {"name": updated_drone_category_name}
        patch_response = self.client.patch(url, data, format="json")
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["name"] == updated_drone_category_name

    def test_get_drone_category(self):
        """
        Ensure we can get a single drone category by id
        """

        drone_category_name = "Easy to retrieve"
        response = self.post_drone_category(drone_category_name)
        url = reverse("dronecategory-detail", None, {response.data.get("pk")})
        get_response = self.client.get(url, format="josn")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["name"] == drone_category_name


class PilotTests(APITestCase):
    def post_pilot(self, name, gender, races_count):
        url = reverse("pilot-list")
        print(url)
        data = {
            "name": name,
            "gender": gender,
            "races_count": races_count,
        }
        response = self.client.post(url, data, format="json")
        return response

    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user("user01", "user01@test.com", "user01P4assw0rD")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_post_and_get_pilot(self):
        """
        Ensure we can create a new pilot and the retrieve it
        Ensure we cannot retrieve the persisted pilot without a token
        """
        self.create_user_and_set_token_credentials()
        new_pilot_name = "Gatson"
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(
            new_pilot_name,
            new_pilot_gender,
            new_pilot_races_count,
        )
        print("PK {0}".format(Pilot.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 1
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.races_count == new_pilot_races_count
        url = reverse("pilot-detail", None, {saved_pilot.pk})
        authorized_get_response = self.client.get(url, format="json")
        assert authorized_get_response == status.HTTP_200_OK
        assert authorized_get_response.data["name"] == new_pilot_name

        # Clean up credentials
        self.client.credentials()

        unauthorized_get_response = self.client.get(url, format="json")
        assert unauthorized_get_response == status.HTTP_401_UNAUTHORIZED