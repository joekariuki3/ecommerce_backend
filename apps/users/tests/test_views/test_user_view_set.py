import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_retrieve_user_profile_success(authenticated_client_and_user):
    """
    Test that an authenticated user can retrieve their profile details.
    """
    client, user = authenticated_client_and_user
    url = reverse("users:me-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["username"] == user.username


@pytest.mark.django_db
def test_update_user_profile(authenticated_client_and_user):
    """
    Test that an authenticated user can update their profile.
    """
    client, user = authenticated_client_and_user
    url = reverse("users:me-detail", kwargs={"pk": user.id})
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
    }
    response = client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Jane"
    assert response.data["last_name"] == "Doe"


@pytest.mark.django_db
def test_delete_user_profile(authenticated_client_and_user):
    """
    Test that an authenticated user can delete their profile.
    """
    client, user = authenticated_client_and_user

    url = reverse("users:me-detail", kwargs={"pk": user.id})

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert get_user_model().objects.count() == 0
