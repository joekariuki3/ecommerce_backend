import csv
import io
from typing import Dict, List

import pytest
from rest_framework import status

from tests.constants import URLs


@pytest.mark.django_db
class TestCategoryDownloadErrors:
    """
    Test suite for the download errors CSV functionality.
    """

    @pytest.fixture
    def download_errors_url(self) -> str:
        """
        Provides the URL for the download errors endpoint.

        Returns:
            str: The download errors URL.
        """
        return URLs.CATEGORY_DOWNLOAD_ERRORS.value

    @pytest.fixture
    def sample_errors_payload(self) -> Dict[str, List[Dict]]:
        """
        Provides a sample JSON payload of errors.

        Returns:
            Dict[str, List[Dict]]: A dictionary containing a list of error objects.
        """
        return {
            "errors": [
                {
                    "row_number": 3,
                    "data": {
                        "name": "Electronics",
                        "description": "A duplicate category",
                    },
                    "errors": {"name": ["category with this name already exists."]},
                },
                {
                    "row_number": 5,
                    "data": {"name": "", "description": "Missing name here"},
                    "errors": {"name": ["This field may not be blank."]},
                },
            ]
        }

    def test_download_errors_as_admin_success(
        self, admin_authenticated_client, download_errors_url, sample_errors_payload
    ):
        """
        Ensure an admin can successfully download a CSV of failed rows.
        """
        response = admin_authenticated_client.post(
            download_errors_url, sample_errors_payload, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.get("Content-Type") == "text/csv"
        assert (
            response.get("Content-Disposition")
            == 'attachment; filename="failed_categories.csv"'
        )

        # Verify CSV content
        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

        # Check header
        assert rows[0] == ["name", "description", "error_details"]
        # Check first data row
        assert rows[1] == [
            "Electronics",
            "A duplicate category",
            "name: category with this name already exists.",
        ]
        # Check second data row
        assert rows[2] == [
            "",
            "Missing name here",
            "name: This field may not be blank.",
        ]

    def test_download_errors_as_regular_user_forbidden(
        self,
        authenticated_client_and_user,
        download_errors_url,
        sample_errors_payload,
    ):
        """
        Ensure a non-admin user receives a 403 Forbidden error.
        """
        client, _ = authenticated_client_and_user
        response = client.post(
            download_errors_url, sample_errors_payload, format="json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_download_errors_with_missing_errors_field(
        self, admin_authenticated_client, download_errors_url
    ):
        """
        Test request with a missing 'errors' field in the payload.
        """
        response = admin_authenticated_client.post(
            download_errors_url, {}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["error"]
            == "The 'errors' field is required and must be a list."
        )

    def test_download_errors_with_invalid_errors_field(
        self, admin_authenticated_client, download_errors_url
    ):
        """
        Test request where 'errors' field is not a list.
        """
        payload = {"errors": "this is not a list"}
        response = admin_authenticated_client.post(
            download_errors_url, payload, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["error"]
            == "The 'errors' field is required and must be a list."
        )
