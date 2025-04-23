# ruff: noqa: S106,S101,S105
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from accounts.models import User
from conftest import user_instance

UserModel = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestOrderCreate:
    def test_order_create_nologin(self, api_client_without_login):
        response = api_client_without_login.post(
            reverse("api_v1:order_create"),
            {"name": "test name", "count": 2, "total_price": 200},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_order_create_bad_input(self, api_client_user):
        response = api_client_user.post(
            reverse("api_v1:order_create"),
            {"name": "test name", "count": "sad", "total_price": 200},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response = api_client_user.post(
            reverse("api_v1:order_create"),
            {"name": "test n<>ame", "count": "sad", "total_price": 200},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "client_fixture,user_fixture",
    [
        ("api_client_user", "normal_user"),
        ("api_client_admin", "admin_user"),
    ],
)
def test_order_create(request, client_fixture, user_fixture):
    client = request.getfixturevalue(client_fixture)
    user = request.getfixturevalue(user_fixture)

    response = client.post(
        reverse("api_v1:order_create"),
        {"name": "good name", "count": 140, "total_price": 200},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "total_price" in response.data
    assert "edited_at" in response.data
    assert "created_at" in response.data
    assert response.data["user"] == user.id
    assert response.data["total_price"] == 200
