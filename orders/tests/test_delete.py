# ruff: noqa: S106,S101,S105
import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Order


@pytest.mark.django_db
class TestOrderDelete:
    def test_order_delete_admin(self, api_client_admin, order3_instance_admin):
        """Test deleting an order via DELETE request by an admin"""
        url = reverse("api_v1:order_delete", kwargs={"pk": order3_instance_admin.pk})

        response = api_client_admin.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Ensure the order is actually deleted
        assert not Order.objects.filter(pk=order3_instance_admin.pk).exists()

    def test_order_delete_non_owner(self, api_client_user, order3_instance_admin):
        """Test that a normal user cannot delete an order that doesn't belong to them"""
        url = reverse("api_v1:order_delete", kwargs={"pk": order3_instance_admin.pk})

        response = api_client_user.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_order_delete_own_order(self, api_client_user, order1_instance):
        """Test that a user can delete their own order"""
        url = reverse("api_v1:order_delete", kwargs={"pk": order1_instance.pk})

        response = api_client_user.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Ensure the order is actually deleted
        assert not Order.objects.filter(pk=order1_instance.pk).exists()

    def test_order_delete_no_permission(self, api_client_without_login):
        """Test that unauthenticated users cannot delete an order"""
        url = reverse(
            "api_v1:order_delete", kwargs={"pk": 1}
        )  # Assuming this order exists

        response = api_client_without_login.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
