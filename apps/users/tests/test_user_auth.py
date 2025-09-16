import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_login_success(api_client, default_user):
    """
    Test a successful user login via the API.
    """
    url = reverse("token_obtain_pair")
    payload = {
        "email": default_user.email,
        "password": "password123",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_user_login_invalid_credentials(api_client, default_user):
    """
    Test that an invalid login attempt is rejected.
    """
    url = reverse("token_obtain_pair")
    payload = {
        "email": default_user.email,
        "password": "wrongpassword",
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "No active account found with the given credentials" in str(
        response.data["detail"]
    )
