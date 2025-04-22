# ruff: noqa: S106,S101,S105,PTH123
import pytest
from rest_framework.test import APIClient

from accounts.models import User


@pytest.fixture
def api_client_with_permissions(user_with_permissions, request) -> APIClient:
    """Fixture for an API client authenticated with a user that has permissions."""
    client = APIClient()

    # Pass the parameter to the user_with_permissions fixture
    user_with_permissions = request.getfixturevalue("user_with_permissions")
    client.force_authenticate(user=user_with_permissions)
    return client


@pytest.fixture
def api_client_without_permissions(user_without_permissions, request) -> APIClient:
    """Fixture for an API client authenticated with a user that has no permissions."""
    client = APIClient()

    # Pass the parameter to the user_with_permissions fixture
    client.force_authenticate(user=user_without_permissions)
    return client


@pytest.fixture
def api_client_without_login(request) -> APIClient:
    """Fixture for an API client with no logedin user"""
    return APIClient()


@pytest.fixture
def user_instance(db, django_user_model) -> tuple[User, str]:
    """Fixture for a user. Returns the password as well in a tuple"""
    return (
        django_user_model.objects.create_user(
            username="testuser", password="password123"
        ),
        "password123",
    )
