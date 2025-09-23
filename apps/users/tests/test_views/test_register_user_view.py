import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_registration_success(api_client):
    """
    Test a successful user registration via the API.
    """
    url = reverse("users:register")
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "strongpassword123",
    }
    response = api_client.post(url, payload, format="json")

    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.data
    assert response.data["username"] == "newuser"
    assert "email" in response.data
    assert get_user_model().objects.count() == 1


@pytest.mark.django_db
def test_user_registration_duplicate_email(api_client, user_factory):
    """
    Test that a user cannot register with an email that already exists.
    """
    user_factory(username="existinguser", email="existing@example.com")

    url = reverse("users:register")
    payload = {
        "username": "newuser",
        "email": "existing@example.com",
        "password": "testpassword",
        "password2": "testpassword",
    }
    response = api_client.post(url, payload, format="json")

    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    assert "user with this email already exists." in str(response.data["email"])
    assert get_user_model().objects.count() == 1
