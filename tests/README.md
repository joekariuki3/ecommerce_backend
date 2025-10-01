# Test Constants Documentation

This document explains the test constants system implemented to avoid hardcoded sensitive data in test fixtures and pass security checks like Bandit.

## Overview

The `tests/constants.py` file contains all test data constants organized into enums and helper functions. This approach:

- ✅ **Passes Bandit security checks** by avoiding hardcoded credentials
- ✅ **Makes tests more maintainable** with centralized constants
- ✅ **Allows environment customization** via environment variables
- ✅ **Provides consistent test data** across all test files

## Structure

### Enums

- **`UserTestData`**: User credentials and data (username, email, password)
- **`TestCategories`**: Category-related test data
- **`TestProducts`**: Product-related test data
- **`TestDatabase`**: Database names for testing
- **`TestAPI`**: API constants like status codes and URLs

### Helper Functions

- **`get_test_user_data(user_type)`**: Returns user data for different user types
- **`get_test_category_data(index, **overrides)`\*\*: Returns category data with optional overrides
- **`get_test_product_data(index, category, **overrides)`\*\*: Returns product data with optional overrides

## Usage Examples

### In Fixtures (`conftest.py`)

```python
from tests.constants import get_test_user_data

@pytest.fixture
def default_user(user_factory):
    user_data = get_test_user_data("default")
    return user_factory(**user_data)
```

### In Test Files

```python
from tests.constants import UserTestData

def test_login(api_client, default_user):
    payload = {
        "email": default_user.email,
        "password": UserTestData.DEFAULT_PASSWORD.value,
    }
```

## Environment Variables

You can customize test data via environment variables in your `.env` file:

```bash
# Test user credentials
TEST_DEFAULT_USERNAME=testuser
TEST_DEFAULT_EMAIL=testuser@example.com
TEST_DEFAULT_PASSWORD=TestPass123!

TEST_ADMIN_USERNAME=adminuser
TEST_ADMIN_EMAIL=adminuser@example.com
TEST_ADMIN_PASSWORD=AdminPass123!
```

## Benefits

1. **Security**: No hardcoded credentials trigger Bandit warnings
2. **Flexibility**: Environment variables allow customization per environment
3. **Maintainability**: Single source of truth for all test data
4. **Consistency**: All tests use the same data format and structure
5. **Documentation**: Clear, self-documenting constants with meaningful names

## Migration from Hardcoded Values

Old approach (triggers Bandit):

```python
def create_user(**kwargs):
    return User.objects.create_user(
        username="testuser",
        email="testuser@mail.com",
        password="password123"
    )
```

New approach (Bandit-safe):

```python
from tests.constants import get_test_user_data

def create_user(**kwargs):
    user_data = get_test_user_data("default")
    user_data.update(kwargs)
    return User.objects.create_user(**user_data)
```

This system ensures tests are secure, maintainable, and follow best practices for handling test data.
