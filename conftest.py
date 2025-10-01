import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product
from tests.constants import (
    get_test_category_data,
    get_test_product_data,
    get_test_user_data,
)


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
    user_data = get_test_user_data("default")
    return user_factory(**user_data)


@pytest.fixture
def admin_user(user_factory):
    """
    Returns a admin User instance.
    """
    user_data = get_test_user_data("admin")
    return user_factory(**user_data)


@pytest.fixture
def superuser(user_factory):
    """
    Returns a superuser instance.
    """
    user_data = get_test_user_data("super")
    return user_factory(**user_data)


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


@pytest.fixture
def create_categories(category_factory):
    """
    A fixture to create multiple Category instances.
    """

    def make_categories(count, **kwargs):
        categories = []
        for i in range(count):
            category_data = get_test_category_data(i, **kwargs)
            categories.append(category_factory(**category_data))
        return categories

    return make_categories


@pytest.fixture
def create_products(product_factory, create_categories):
    """
    A fixture to create multiple Product instances.
    """

    def make_products(count, **kwargs):
        products = []
        categories = create_categories(5)
        for i in range(count):
            category = categories[i % len(categories)]  # Round-robin assignment
            product_data = get_test_product_data(i, category=category, **kwargs)
            products.append(product_factory(**product_data))
        return products

    return make_products
