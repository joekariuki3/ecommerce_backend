"""
Test constants and enums to avoid hardcoding sensitive data in test fixtures.
This helps pass security checks like Bandit and makes tests more maintainable.
"""

import os
from enum import Enum


class UserTestData(Enum):
    """Test user data constants."""

    DEFAULT_USERNAME = os.getenv("TEST_DEFAULT_USERNAME", "testuser")
    DEFAULT_EMAIL = os.getenv("TEST_DEFAULT_EMAIL", "testuser@example.com")
    DEFAULT_PASSWORD = os.getenv("TEST_DEFAULT_PASSWORD", "TestPass123!")

    ADMIN_USERNAME = os.getenv("TEST_ADMIN_USERNAME", "adminuser")
    ADMIN_EMAIL = os.getenv("TEST_ADMIN_EMAIL", "adminuser@example.com")
    ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD", "AdminPass123!")

    SUPER_USERNAME = os.getenv("TEST_SUPER_USERNAME", "superuser")
    SUPER_EMAIL = os.getenv("TEST_SUPER_EMAIL", "superuser@example.com")
    SUPER_PASSWORD = os.getenv("TEST_SUPER_PASSWORD", "SuperPass123!")

    WRONG_PASSWORD = "WrongPass123!"


class TestCategories(Enum):
    """Test category data constants."""

    DEFAULT_NAME_PREFIX = "Test Category"
    DEFAULT_DESCRIPTION_PREFIX = "Test description for category"

    ELECTRONICS = "Electronics"
    BOOKS = "Books"
    CLOTHING = "Clothing"
    SPORTS = "Sports"
    HOME = "Home & Garden"


class TestProducts(Enum):
    """Test product data constants."""

    DEFAULT_NAME_PREFIX = "Test Product"
    DEFAULT_DESCRIPTION_PREFIX = "Test description for product"
    DEFAULT_BASE_PRICE = 10.0

    LAPTOP = "Test Laptop"
    BOOK = "Test Book"
    SHIRT = "Test Shirt"
    BALL = "Test Ball"
    CHAIR = "Test Chair"


class TestDatabase(Enum):
    """Test database constants."""

    DEFAULT_DB_NAME = os.getenv("TEST_DB_NAME", "test_ecommerce_db")
    SQLITE_DB_NAME = os.getenv("TEST_SQLITE_DB_NAME", "test_db")


class TestAPI(Enum):
    """Test API constants."""

    BASE_URL = "/api/"

    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404


def get_test_user_data(user_type: str = "default") -> dict:
    """
    Get test user data based on user type.

    Args:
        user_type: Type of user ('default', 'admin', 'super')

    Returns:
        Dictionary with user data
    """
    user_data_map = {
        "default": {
            "username": UserTestData.DEFAULT_USERNAME.value,
            "email": UserTestData.DEFAULT_EMAIL.value,
            "password": UserTestData.DEFAULT_PASSWORD.value,
        },
        "admin": {
            "username": UserTestData.ADMIN_USERNAME.value,
            "email": UserTestData.ADMIN_EMAIL.value,
            "password": UserTestData.ADMIN_PASSWORD.value,
            "is_staff": True,
        },
        "super": {
            "username": UserTestData.SUPER_USERNAME.value,
            "email": UserTestData.SUPER_EMAIL.value,
            "password": UserTestData.SUPER_PASSWORD.value,
            "is_superuser": True,
        },
    }

    return user_data_map.get(user_type, user_data_map["default"])


def get_test_category_data(index: int = 0, **overrides) -> dict:
    """
    Get test category data with optional overrides.

    Args:
        index: Index for generating unique names
        **overrides: Override any default values

    Returns:
        Dictionary with category data
    """
    data = {
        "name": f"{TestCategories.DEFAULT_NAME_PREFIX.value} {index + 1}",
        "description": f"{TestCategories.DEFAULT_DESCRIPTION_PREFIX.value} {index + 1}",
    }
    data.update(overrides)
    return data


def get_test_product_data(index: int = 0, category=None, **overrides) -> dict:
    """
    Get test product data with optional overrides.

    Args:
        index: Index for generating unique names
        category: Category instance to associate with product
        **overrides: Override any default values

    Returns:
        Dictionary with product data
    """
    data = {
        "name": f"{TestProducts.DEFAULT_NAME_PREFIX.value} {index + 1}",
        "description": f"{TestProducts.DEFAULT_DESCRIPTION_PREFIX.value} {index + 1}",
        "price": TestProducts.DEFAULT_BASE_PRICE.value + index,
    }

    if category:
        data["category"] = category

    data.update(overrides)
    return data
