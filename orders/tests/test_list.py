# ruff: noqa: S106,S101,S105
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from accounts.models import User
from orders.models import Order


class TestOrderList:
    def test_order_list_nologin(self, api_client_without_login):
        response = api_client_without_login.get(reverse("api_v1:order_list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_order_list_normal_user(self, api_client_user, normal_user):
        # Create 2 orders for normal user, 1 for someone else
        Order.objects.create(name="Order A", count=2, total_price=100, user=normal_user)
        other_user = User.objects.create_user(username="other", password="1234")
        Order.objects.create(name="Order B", count=1, total_price=999, user=other_user)

        response = api_client_user.get(reverse("api_v1:order_list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["user"] == normal_user.id

    def test_order_list_admin_user(self, api_client_admin, admin_user):
        # Create orders for multiple users
        user1 = User.objects.create_user(username="user1", password="pass")
        user2 = User.objects.create_user(username="user2", password="pass")

        Order.objects.create(name="Order 1", count=2, total_price=100, user=admin_user)
        Order.objects.create(name="Order 2", count=1, total_price=200, user=user1)
        Order.objects.create(name="Order 3", count=5, total_price=300, user=user2)

        response = api_client_admin.get(reverse("api_v1:order_list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_order_list_filter_price(self, api_client_admin, admin_user):
        # Create 3 orders with different prices
        Order.objects.create(name="Low", count=1, total_price=50, user=admin_user)
        Order.objects.create(name="Medium", count=1, total_price=150, user=admin_user)
        Order.objects.create(name="High", count=1, total_price=300, user=admin_user)

        url = reverse("api_v1:order_list")
        response = api_client_admin.get(f"{url}?min_price=100&max_price=200")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Medium"


@pytest.mark.django_db
class TestOrderListFilters:
    @pytest.fixture
    def seeded_orders(self, admin_user):
        now = timezone.now()
        return [
            Order.objects.create(
                name="Cheap Old",
                count=1,
                total_price=30,
                user=admin_user,
                created_at=now - timedelta(days=15),
            ),
            Order.objects.create(
                name="Cheap Recent",
                count=1,
                total_price=30,
                user=admin_user,
                created_at=now - timedelta(days=3),
            ),
            Order.objects.create(
                name="Mid",
                count=2,
                total_price=150,
                user=admin_user,
                created_at=now - timedelta(days=5),
            ),
            Order.objects.create(
                name="Expensive",
                count=3,
                total_price=300,
                user=admin_user,
                created_at=now - timedelta(days=1),
            ),
            Order.objects.create(
                name="Very Expensive",
                count=4,
                total_price=500,
                user=admin_user,
                created_at=now,
            ),
            Order.objects.create(
                name="Outlier",
                count=10,
                total_price=9999,
                user=admin_user,
                created_at=now - timedelta(days=100),
            ),
        ]

    def test_filter_exact_price(self, api_client_admin, seeded_orders):
        url = reverse("api_v1:order_list")
        response = api_client_admin.get(f"{url}?price=150")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Mid"

    def test_filter_min_price(self, api_client_admin, seeded_orders):
        url = reverse("api_v1:order_list")
        response = api_client_admin.get(f"{url}?min_price=100")
        assert response.status_code == status.HTTP_200_OK
        assert all(order["total_price"] >= 100 for order in response.data)

    def test_filter_max_price(self, api_client_admin, seeded_orders):
        url = reverse("api_v1:order_list")
        response = api_client_admin.get(f"{url}?max_price=100")
        assert response.status_code == status.HTTP_200_OK
        assert all(order["total_price"] <= 100 for order in response.data)

    def test_filter_date_after(self, api_client_admin, seeded_orders):
        date_str = (timezone.now() - timedelta(days=6)).strftime("%Y-%m-%d")
        url = reverse("api_v1:order_list")
        response = api_client_admin.get(f"{url}?date_after={date_str}")
        assert response.status_code == status.HTTP_200_OK
        assert all(order["created_at"] >= date_str for order in response.data)

    def test_filter_date_before(self, api_client_admin, seeded_orders):
        date_str = (timezone.now() - timedelta(days=6)).strftime("%Y-%m-%d")
        url = reverse("api_v1:order_list")
        response = api_client_admin.get(f"{url}?date_before={date_str}")
        assert response.status_code == status.HTTP_200_OK
        assert all(order["created_at"] <= date_str for order in response.data)
