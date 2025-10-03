import os
import tempfile
from io import BytesIO

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
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
def default_category(category_factory):
    """
    Returns a default Category instance.
    """
    category_data = get_test_category_data()
    return category_factory(**category_data)


@pytest.fixture
def product_factory():
    """
    A factory fixture to create Product instances with optional keyword arguments.
    """

    def create_product(**kwargs):
        return Product.objects.create(**kwargs)

    return create_product


@pytest.fixture
def default_product(product_factory, default_category):
    """
    Returns a default Product instance.
    """
    product_data = get_test_product_data(category=default_category)
    return product_factory(**product_data)


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


@pytest.fixture()
def temp_media_root():
    """Create a temporary directory for media files during tests."""
    temp_dir = tempfile.mkdtemp()
    with override_settings(MEDIA_ROOT=temp_dir):
        yield temp_dir


@pytest.fixture
def test_image():
    """Create a test image file."""

    def _create_image(width=100, height=100, color="red", format="JPEG"):
        image = Image.new("RGB", (width, height), color=color)
        temp_file = BytesIO()
        image.save(temp_file, format=format)
        temp_file.seek(0)
        return SimpleUploadedFile(
            name="test.jpg", content=temp_file.getvalue(), content_type="image/jpeg"
        )

    return _create_image


@pytest.fixture
def large_test_image():
    """Create a large test image (> 5MB) using random bytes."""
    width, height = 2000, 2000

    total_bytes = width * height * 3

    # Creating large amount of random bytes (data)
    random_bytes = os.urandom(total_bytes)

    image = Image.frombytes("RGB", (width, height), random_bytes)

    temp_file = BytesIO()

    image.save(temp_file, format="JPEG", quality=100, optimize=False)
    temp_file.seek(0)

    # Verify the image is actually larger than 5MB
    file_size = len(temp_file.getvalue())
    assert (
        file_size > 5 * 1024 * 1024
    ), f"Test image is only {file_size / 1024 / 1024:.2f}MB, should be > 5MB"

    return SimpleUploadedFile(
        name="large.jpg", content=temp_file.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def invalid_file():
    """Create an invalid file (not an image)."""
    return SimpleUploadedFile(
        name="test.txt", content=b"This is not an image", content_type="text/plain"
    )
