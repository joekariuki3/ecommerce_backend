import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.catalog.models import Category, Product


@pytest.fixture
def user_factory():
    """
    A factory fixture to create a User instance with optional keyword arguments.
    """

    def create_user(**kwargs):
        User = get_user_model()
        return User.objects.create_user(**kwargs)

    return create_user


@pytest.fixture
def default_user(user_factory):
    """
    Returns a simple, non-admin User instance.
    """
    return user_factory(
        username="testuser", email="testuser@mail.com", password="password123"
    )


@pytest.fixture
def admin_user(user_factory):
    """
    Returns a admin User instance.
    """
    return user_factory(
        username="adminuser",
        email="adminuser@mail.com",
        password="password123",
        is_staff=True,
    )


@pytest.fixture
def superuser(user_factory):
    """
    Returns a superuser instance.
    """
    return user_factory(
        username="superuser",
        email="superuser@mail.com",
        password="password123",
        is_superuser=True,
    )


@pytest.fixture
def api_client():
    """
    A test client instance.
    """
    return APIClient()


@pytest.fixture
def authenticated_client_and_user(default_user):
    """
    Returns a tuple containing an authenticated test client and the user object.
    """
    client = APIClient()
    client.force_authenticate(user=default_user)
    return client, default_user


@pytest.fixture
def admin_authenticated_client(admin_user):
    """
    An admin-authenticated test client.
    """
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def category_factory():
    """
    A factory fixture to create Category instances with optional keyword arguments.
    """

    def create_category(**kwargs):
        return Category.objects.create(**kwargs)

    return create_category


@pytest.fixture
def product_factory():
    """
    A factory fixture to create Product instances with optional keyword arguments.
    """

    def create_product(**kwargs):
        return Product.objects.create(**kwargs)

    return create_product
