# ruff: noqa: S106,S101,S105
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from accounts.models import User

UserModel = get_user_model()


@pytest.mark.django_db
def test_token_obtain_success(
    api_client_without_login, user_instance: tuple[User, str]
):
    response = api_client_without_login.post(
        reverse("api_v1:token_obtain_pair"),
        {"username": user_instance[0].username, "password": user_instance[1]},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_obtain_fail_wrong_credentials(api_client_without_login, user_instance):
    response = api_client_without_login.post(
        reverse("api_v1:token_obtain_pair"),
        {"username": "wronguser", "password": "wrong"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_token_refresh_success(api_client_without_login, user_instance):
    token_response = api_client_without_login.post(
        reverse("api_v1:token_obtain_pair"),
        {"username": user_instance[0].username, "password": user_instance[1]},
    )

    refresh_token = token_response.data["refresh"]
    response = api_client_without_login.post(
        reverse("api_v1:token_refresh"), {"refresh": refresh_token}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_token_refresh_fail_invalid_token(api_client_without_login, user_instance):
    response = api_client_without_login.post(
        reverse("api_v1:token_refresh"), {"refresh": "notarealtoken"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
