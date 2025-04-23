# ruff: noqa: S106,S101,S105
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestOrderUpdate:
    def test_order_update_put(self, api_client_admin, order3_instance_admin):
        """Test updating an order via PUT request by an admin"""
        url = reverse("api_v1:order_update", kwargs={"pk": order3_instance_admin.pk})
        data = {
            "name": "Updated Order C",
            "count": 5,
            "total_price": 1500,
        }

        response = api_client_admin.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Order C"
        assert response.data["count"] == 5
        assert response.data["total_price"] == 1500

    def test_order_update_patch(self, api_client_admin, order3_instance_admin):
        """Test updating an order via PATCH request by an admin"""
        url = reverse("api_v1:order_update", kwargs={"pk": order3_instance_admin.pk})
        data = {
            "total_price": 3500,
        }

        response = api_client_admin.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_price"] == 3500

    def test_order_update_no_permission(
        self, api_client_without_login, order1_instance
    ):
        """Test that a user without permission can't update an order"""
        url = reverse("api_v1:order_update", kwargs={"pk": order1_instance.pk})
        data = {
            "name": "Attempted Update",
            "count": 3,
            "total_price": 300,
        }

        response = api_client_without_login.put(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_order_update_non_owner(self, api_client_user, order3_instance_admin):
        """Test that a normal user cannot update an order that doesn't belong to them"""
        # Ensure the other user's order is different
        url = reverse("api_v1:order_update", kwargs={"pk": order3_instance_admin.pk})
        data = {
            "name": "Attempted Update by non-owner",
            "count": 3,
            "total_price": 600,
        }

        response = api_client_user.put(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_order_update_own_order(self, api_client_user, order1_instance):
        """Test that a user can update their own order"""
        url = reverse("api_v1:order_update", kwargs={"pk": order1_instance.pk})
        data = {
            "name": "Updated Order A",
            "count": 3,
            "total_price": 300,
        }

        response = api_client_user.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Order A"
        assert response.data["count"] == 3
        assert response.data["total_price"] == 300
