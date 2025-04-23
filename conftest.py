# ruff: noqa: S106,S101,S105,PTH123
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient

from accounts.models import User
from orders.models import Order

UserModel = get_user_model()


@pytest.fixture
def admin_group(db):
    group, _ = Group.objects.get_or_create(name="admin")
    perms = Permission.objects.filter(
        codename__in=["edit_all_orders", "view_all_orders", "delete_all_orders"]
    )
    group.permissions.set(perms)
    return group


@pytest.fixture
def normal_user_group(db):
    group, _ = Group.objects.get_or_create(name="normal_user")
    # No custom permissions added — uses object-level access.
    return group


@pytest.fixture
def admin_user(admin_group) -> User:
    user = User.objects.create_user(username="admin", password="adminpass")
    user.groups.add(admin_group)
    return user


@pytest.fixture
def normal_user(normal_user_group) -> User:
    user = User.objects.create_user(username="normal", password="userpass")
    user.groups.add(normal_user_group)
    return user


@pytest.fixture
def api_client_admin(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def api_client_user(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
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


@pytest.fixture
def order1_instance(db, normal_user) -> Order:
    return Order.objects.create(
        name="Order A", count=2, total_price=100, user=normal_user
    )


@pytest.fixture
def order2_instance(db, normal_user) -> Order:
    return Order.objects.create(
        name="Order B", count=2, total_price=250, user=normal_user
    )


@pytest.fixture
def order3_instance_admin(db, admin_user) -> Order:
    return Order.objects.create(
        name="Order C", count=2, total_price=300, user=admin_user
    )
