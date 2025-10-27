import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from apps.catalog.models import Category
from tests.constants import URLs


@pytest.mark.django_db
class TestCategoryBulkUpload:
    """
    Test suite for the bulk category upload functionality.
    """

    @pytest.fixture
    def bulk_upload_url(self):
        """Fixture for the bulk upload URL."""
        return URLs.CATEGORY_BULK_UPLOAD_URL.value

    def create_csv_file(self, content):
        """Helper to create an in-memory CSV file for uploading."""
        return SimpleUploadedFile("categories.csv", content.encode("utf-8"), "text/csv")

    def test_bulk_upload_as_admin_success(
        self, admin_authenticated_client, bulk_upload_url
    ):
        """
        Ensure an admin can successfully bulk upload categories from a valid CSV.
        Expects a 200 OK status for a fully successful upload.
        """
        csv_content = "name,description\nElectronics,All electronic gadgets\nBooks,A wide range of books"
        csv_file = self.create_csv_file(csv_content)

        response = admin_authenticated_client.post(
            bulk_upload_url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "Upload completed successfully."
        assert response.data["success_count"] == 2
        assert response.data["error_count"] == 0
        assert len(response.data["errors"]) == 0
        assert Category.objects.count() == 2
        assert Category.objects.filter(name="Electronics").exists()
        assert Category.objects.filter(name="Books").exists()

    def test_bulk_upload_as_regular_user_forbidden(
        self, authenticated_client_and_user, bulk_upload_url
    ):
        """
        Ensure a non-admin user receives a 403 Forbidden error.
        """
        client, _ = authenticated_client_and_user
        csv_content = "name,description\nForbidden,Should not be created"
        csv_file = self.create_csv_file(csv_content)

        response = client.post(bulk_upload_url, {"file": csv_file}, format="multipart")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Category.objects.count() == 0

    def test_bulk_upload_with_mixed_data_returns_207(
        self, admin_authenticated_client, bulk_upload_url, category_factory
    ):
        """
        Test uploading a CSV with both valid and invalid rows.
        Expects a 207 Multi-Status for partial success.
        """
        # Pre-existing category to test duplicate handling
        category_factory(name="Electronics")

        csv_content = (
            "name,description\n"
            "Books,A new category\n"  # Valid
            "Electronics,A duplicate category\n"  # Invalid (duplicate)
            ",A category with no name"  # Invalid (missing name)
        )
        csv_file = self.create_csv_file(csv_content)

        response = admin_authenticated_client.post(
            bulk_upload_url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_207_MULTI_STATUS
        assert response.data["status"] == "Upload completed with 2 errors."
        assert response.data["success_count"] == 1
        assert response.data["error_count"] == 2

        # Check errors
        errors = response.data["errors"]
        assert len(errors) == 2

        # Error 1: Duplicate name
        assert errors[0]["row_number"] == 3
        assert errors[0]["data"]["name"] == "Electronics"
        assert "name" in errors[0]["errors"]
        assert (
            "category with this name already exists." in errors[0]["errors"]["name"][0]
        )

        # Error 2: Missing name
        assert errors[1]["row_number"] == 4
        assert errors[1]["data"]["name"] == ""
        assert "name" in errors[1]["errors"]
        assert "This field may not be blank." in errors[1]["errors"]["name"][0]

        # Verify database state (only 1 new category should be created)
        assert Category.objects.count() == 2  # 1 pre-existing + 1 new
        assert Category.objects.filter(name="Books").exists()

    def test_bulk_upload_with_all_rows_failing_returns_400(
        self, admin_authenticated_client, bulk_upload_url, category_factory
    ):
        """
        Test uploading a CSV where all data rows are invalid.
        Expects a 400 Bad Request status.
        """
        category_factory(name="Electronics")

        csv_content = (
            "name,description\n"
            "Electronics,A duplicate category\n"  # Invalid (duplicate)
            ",A category with no name"  # Invalid (missing name)
        )
        csv_file = self.create_csv_file(csv_content)

        response = admin_authenticated_client.post(
            bulk_upload_url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "Upload completed with 2 errors."
        assert response.data["success_count"] == 0
        assert response.data["error_count"] == 2
        assert len(response.data["errors"]) == 2
        assert Category.objects.count() == 1  # Only the pre-existing one

    def test_bulk_upload_missing_header(
        self, admin_authenticated_client, bulk_upload_url
    ):
        """
        Test uploading a CSV with a missing required 'name' header.
        Expects a 400 Bad Request status.
        """
        csv_content = "description\nJust a description"
        csv_file = self.create_csv_file(csv_content)

        response = admin_authenticated_client.post(
            bulk_upload_url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "Error"
        assert response.data["error_count"] == 1
        assert (
            "Missing required columns: name"
            in response.data["errors"][0]["errors"]["headers"]
        )
        assert Category.objects.count() == 0

    def test_bulk_upload_no_file(self, admin_authenticated_client, bulk_upload_url):
        """
        Test making a POST request without a file.
        """
        response = admin_authenticated_client.post(
            bulk_upload_url, {}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "No file uploaded."

    def test_bulk_upload_invalid_csv_format(
        self, admin_authenticated_client, bulk_upload_url
    ):
        """
        Test uploading a file that is not a valid CSV.
        """
        # Using a binary file content to simulate a non-text file
        invalid_file = SimpleUploadedFile(
            "file.bin", b"\x80\x81\x82", "application/octet-stream"
        )

        response = admin_authenticated_client.post(
            bulk_upload_url, {"file": invalid_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "Error"
        assert "Invalid CSV file format" in response.data["errors"][0]["errors"]["file"]
        assert Category.objects.count() == 0
