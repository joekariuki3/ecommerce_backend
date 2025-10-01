import pytest
from django.urls import reverse
from rest_framework import status

from tests.constants import TestUsers


@pytest.mark.django_db
def test_user_login_success(api_client, default_user):
    """
    Test a successful user login via the API.
    """
    url = reverse("login")
    payload = {
        "email": default_user.email,
        "password": TestUsers.DEFAULT_PASSWORD.value,
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
    url = reverse("login")
    payload = {
        "email": default_user.email,
        "password": TestUsers.WRONG_PASSWORD.value,  # Incorrect password
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "No active account found with the given credentials" in str(
        response.data["detail"]
    )


@pytest.mark.django_db
def test_user_login_missing_fields(api_client):
    """
    Test that login fails when required fields are missing.
    """
    url = reverse("login")
    payload = {
        "email": "",
        "password": "",
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in str(response.data["email"])
    assert "This field may not be blank." in str(response.data["password"])


@pytest.mark.django_db
def test_user_logout_success(api_client, default_user):
    """
    Test a successful user logout via the API.
    """
    # First, log in to get a refresh token
    login_url = reverse("login")
    login_payload = {
        "email": default_user.email,
        "password": TestUsers.DEFAULT_PASSWORD.value,
    }
    login_response = api_client.post(login_url, login_payload, format="json")
    refresh_token = login_response.data["refresh"]

    # Now, log out using the refresh token
    logout_url = reverse("logout")
    logout_payload = {
        "refresh": refresh_token,
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
    logout_response = api_client.post(logout_url, logout_payload, format="json")

    assert logout_response.status_code == status.HTTP_205_RESET_CONTENT
    assert logout_response.data["success"] is True
    assert logout_response.data["message"] == "Successfully logged out."


@pytest.mark.django_db
def test_user_token_refresh_success(api_client, default_user):
    """
    Test a successful token refresh via the API.
    """
    # First, log in to get a refresh token
    login_url = reverse("login")
    login_payload = {
        "email": default_user.email,
        "password": TestUsers.DEFAULT_PASSWORD.value,
    }
    login_response = api_client.post(login_url, login_payload, format="json")
    refresh_token = login_response.data["refresh"]

    # Now, refresh the access token using the refresh token
    refresh_url = reverse("token_refresh")
    refresh_payload = {
        "refresh": refresh_token,
    }
    refresh_response = api_client.post(refresh_url, refresh_payload, format="json")

    assert refresh_response.status_code == status.HTTP_200_OK
    assert "access" in refresh_response.data
    assert refresh_response.data["access"] != login_response.data["access"]


@pytest.mark.django_db
def test_user_token_refresh_invalid_token(api_client):
    """
    Test that token refresh fails with an invalid refresh token.
    """
    refresh_url = reverse("token_refresh")
    refresh_payload = {
        "refresh": "invalidtoken",
    }
    refresh_response = api_client.post(refresh_url, refresh_payload, format="json")

    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Token is invalid" in str(refresh_response.data["detail"])


@pytest.mark.django_db
def test_user_token_refresh_missing_token(api_client):
    """
    Test that token refresh fails when the refresh token is missing.
    """
    refresh_url = reverse("token_refresh")
    refresh_payload = {}
    refresh_response = api_client.post(refresh_url, refresh_payload, format="json")

    assert refresh_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field is required." in str(refresh_response.data["refresh"])
