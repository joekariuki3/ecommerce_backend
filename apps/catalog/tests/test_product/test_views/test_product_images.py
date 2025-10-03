import os
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status

from apps.catalog.models import Product
from tests.constants import Formats, URLs, get_test_product_data


@pytest.mark.django_db
class TestProductImageUpload:
    """Test product image upload functionality."""

    def test_create_product_with_image_success(
        self, admin_authenticated_client, default_category, test_image, temp_media_root
    ):
        """Test creating a product with a valid image."""
        image_file = test_image()

        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)
        product_data["image"] = image_file

        response = admin_authenticated_client.post(
            URLs.PRODUCT_LIST.value, product_data, format=Formats.MULTIPART.value
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "image" in response.data
        assert response.data["image"] is not None

        # Verify product was created with image
        product = Product.objects.get(id=response.data["id"])
        assert product.image is not None
        assert product.image.name.startswith("products/")

    def test_create_product_without_image_success(
        self, admin_authenticated_client, default_category, temp_media_root
    ):
        """Test creating a product without an image."""
        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)

        response = admin_authenticated_client.post(
            URLs.PRODUCT_LIST.value, product_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["image"] is None

        # Verify product was created without image
        product = Product.objects.get(id=response.data["id"])
        assert not product.image

    def test_unauthorized_user_cannot_upload_image(
        self, api_client, default_category, test_image, temp_media_root
    ):
        """Test that unauthorized users cannot upload product images."""
        image_file = test_image()

        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)
        product_data["image"] = image_file

        response = api_client.post(
            URLs.PRODUCT_LIST.value, product_data, format=Formats.MULTIPART.value
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cannot_upload_image(
        self,
        authenticated_client_and_user,
        default_category,
        test_image,
        temp_media_root,
    ):
        """Test that regular users cannot upload product images."""
        client, _ = authenticated_client_and_user
        image_file = test_image()

        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)
        product_data["image"] = image_file

        response = client.post(
            URLs.PRODUCT_LIST.value, product_data, format=Formats.MULTIPART.value
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestProductImageUpdate:
    """Test product image update functionality."""

    def test_update_product_add_image(
        self, admin_authenticated_client, default_product, test_image, temp_media_root
    ):
        """Test adding an image to an existing product."""
        assert not default_product.image  # Product starts without image

        image_file = test_image()
        data = {"image": image_file}

        response = admin_authenticated_client.patch(
            URLs.PRODUCT_DETAIL.value.format(product_id=default_product.id),
            data,
            format=Formats.MULTIPART.value,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["image"] is not None

        # Verify image was added
        default_product.refresh_from_db()
        assert default_product.image is not None

    def test_update_product_replace_image(
        self,
        admin_authenticated_client,
        product_factory,
        default_category,
        test_image,
        temp_media_root,
    ):
        """Test replacing an existing product image."""
        # Create product with initial image
        initial_image = test_image(color="blue")
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = initial_image
        product = product_factory(**product_data)

        original_image_path = product.image.path

        # Update with new image
        new_image = test_image(color="green")
        data = {"image": new_image}

        response = admin_authenticated_client.patch(
            URLs.PRODUCT_DETAIL.value.format(product_id=product.id),
            data,
            format=Formats.MULTIPART.value,
        )

        assert response.status_code == status.HTTP_200_OK

        # Verify image was replaced
        product.refresh_from_db()
        assert product.image is not None
        assert product.image.path != original_image_path

    def test_update_other_fields_keeps_image(
        self,
        admin_authenticated_client,
        product_factory,
        default_category,
        test_image,
        temp_media_root,
    ):
        """Test that updating other fields doesn't affect the image."""
        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product = product_factory(**product_data)

        # Verify product has image initially
        assert product.image is not None
        assert os.path.exists(product.image.path)

        # Update only the name (not the image)
        data = {"name": "Updated Product Name"}

        response = admin_authenticated_client.patch(
            URLs.PRODUCT_DETAIL.value.format(product_id=product.id),
            data,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Product Name"

        # Verify image is still there and functional
        product.refresh_from_db()
        assert product.image is not None
        assert product.image.name.startswith("products/")
        assert os.path.exists(product.image.path)

        # Verify the API response still includes the image
        assert response.data["image"] is not None
        assert "/media/products/" in response.data["image"]


@pytest.mark.django_db
class TestProductImageValidation:
    """Test product image validation."""

    def test_image_too_large_rejected(
        self,
        admin_authenticated_client,
        default_category,
        large_test_image,
        temp_media_root,
    ):
        """Test that images larger than 5MB are rejected."""
        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)
        product_data["image"] = large_test_image

        response = admin_authenticated_client.post(
            URLs.PRODUCT_LIST.value, product_data, format=Formats.MULTIPART.value
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "image" in response.data
        assert (
            "image size should not exceed 5mb" in str(response.data["image"][0]).lower()
        )

    def test_invalid_image_format_rejected(
        self,
        admin_authenticated_client,
        default_category,
        invalid_file,
        temp_media_root,
    ):
        """Test that non-image files are rejected."""
        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)
        product_data["image"] = invalid_file

        response = admin_authenticated_client.post(
            URLs.PRODUCT_LIST.value, product_data, format=Formats.MULTIPART.value
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "image" in response.data
        assert "upload a valid image" in str(response.data["image"][0]).lower()

    def test_supported_image_formats(
        self, admin_authenticated_client, default_category, temp_media_root
    ):
        """Test that all supported image formats are accepted."""
        supported_formats = [
            ("JPEG", "image/jpeg", "test.jpg"),
            ("PNG", "image/png", "test.png"),
            ("WEBP", "image/webp", "test.webp"),
        ]

        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)

        for img_format, content_type, filename in supported_formats:
            image = Image.new("RGB", (100, 100), color="red")
            temp_file = BytesIO()
            image.save(temp_file, format=img_format)
            temp_file.seek(0)

            image_file = SimpleUploadedFile(
                name=filename, content=temp_file.getvalue(), content_type=content_type
            )

            product_data["image"] = image_file

            response = admin_authenticated_client.post(
                URLs.PRODUCT_LIST.value,
                product_data,
                format=Formats.MULTIPART.value,
            )

            assert (
                response.status_code == status.HTTP_201_CREATED
            ), f"Failed for {img_format}"
            assert response.data["image"] is not None


@pytest.mark.django_db
class TestProductImageRemoval:
    """Test product image removal functionality."""

    def test_remove_image_endpoint_success(
        self,
        admin_authenticated_client,
        product_factory,
        default_category,
        test_image,
        temp_media_root,
    ):
        """Test removing a product image via the remove_image endpoint."""
        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product = product_factory(**product_data)

        assert product.image  # Verify product has image

        response = admin_authenticated_client.delete(
            URLs.PRODUCT_REMOVE_IMAGE.value.format(product_id=product.id)
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "Image removed successfully"

        # Verify image was removed
        product.refresh_from_db()
        assert not product.image

    def test_remove_image_no_image_exists(
        self, admin_authenticated_client, default_product, temp_media_root
    ):
        """Test removing image from product that has no image."""
        assert not default_product.image  # Product has no image

        response = admin_authenticated_client.delete(
            URLs.PRODUCT_REMOVE_IMAGE.value.format(product_id=default_product.id)
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "No image to delete."

    def test_remove_image_unauthorized(
        self, api_client, product_factory, default_category, test_image, temp_media_root
    ):
        """Test that unauthorized users cannot remove images."""
        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product = product_factory(**product_data)

        response = api_client.delete(
            URLs.PRODUCT_REMOVE_IMAGE.value.format(product_id=product.id)
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_remove_image_regular_user_forbidden(
        self,
        authenticated_client_and_user,
        product_factory,
        default_category,
        test_image,
        temp_media_root,
    ):
        """Test that regular users cannot remove images."""
        client, _ = authenticated_client_and_user

        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product = product_factory(**product_data)

        response = client.delete(
            URLs.PRODUCT_REMOVE_IMAGE.value.format(product_id=product.id)
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestProductImageInListing:
    """Test product image URLs in API responses."""

    def test_product_list_includes_image(
        self, api_client, product_factory, default_category, test_image, temp_media_root
    ):
        """Test that product list includes image URLs."""
        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product_factory(**product_data)

        # Create product without image
        product_data_no_img = get_test_product_data(1, category=default_category)
        product_factory(**product_data_no_img)

        response = api_client.get(URLs.PRODUCT_LIST.value)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

        # Check that both products have image field
        for product in response.data["results"]:
            assert "image" in product

        # One should have image, one should be null
        images = [p["image"] for p in response.data["results"]]
        assert None in images
        assert any(url is not None for url in images)

    def test_product_detail_includes_image(
        self, api_client, product_factory, default_category, test_image, temp_media_root
    ):
        """Test that product detail includes image URL."""
        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product = product_factory(**product_data)

        response = api_client.get(
            URLs.PRODUCT_DETAIL.value.format(product_id=product.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert "image" in response.data
        assert response.data["image"] is not None
        assert "/media/products/" in response.data["image"]

    def test_product_without_image_has_null_url(
        self, api_client, default_product, temp_media_root
    ):
        """Test that products without images have null image."""
        response = api_client.get(
            URLs.PRODUCT_DETAIL.value.format(product_id=default_product.id)
        )

        assert response.status_code == status.HTTP_200_OK
        assert "image" in response.data
        assert response.data["image"] is None


@pytest.mark.django_db
class TestProductImageDeletion:
    """Test image cleanup when products are deleted."""

    def test_image_deleted_with_product(
        self,
        admin_authenticated_client,
        product_factory,
        default_category,
        test_image,
        temp_media_root,
    ):
        """Test that image files are deleted when product is deleted."""
        # Create product with image
        image_file = test_image()
        product_data = get_test_product_data(0, category=default_category)
        product_data["image"] = image_file
        product = product_factory(**product_data)

        image_path = product.image.path
        assert os.path.exists(image_path)  # Verify image file exists

        # Delete product
        response = admin_authenticated_client.delete(
            URLs.PRODUCT_DETAIL.value.format(product_id=product.id)
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify image file was also deleted
        assert not os.path.exists(image_path)


@pytest.mark.django_db
class TestProductImageCompression:
    """Test image compression and resizing functionality."""

    def test_large_image_gets_compressed(
        self, admin_authenticated_client, default_category, temp_media_root
    ):
        """Test that large images are compressed and resized."""
        # Create a large image (within size limit but dimensions > 800x600)
        large_image = Image.new("RGB", (1200, 900), color="red")
        temp_file = BytesIO()
        large_image.save(temp_file, format="JPEG", quality=100)
        temp_file.seek(0)

        image_file = SimpleUploadedFile(
            name="large.jpg", content=temp_file.getvalue(), content_type="image/jpeg"
        )

        product_data = get_test_product_data()
        product_data["category_id"] = str(default_category.id)
        product_data["image"] = image_file

        response = admin_authenticated_client.post(
            URLs.PRODUCT_LIST.value, product_data, format=Formats.MULTIPART.value
        )

        assert response.status_code == status.HTTP_201_CREATED

        # Verify image was created and check its dimensions
        product = Product.objects.get(id=response.data["id"])
        assert product.image is not None

        # Check that image was resized (should be <= 800x600)
        with Image.open(product.image.path) as img:
            assert img.size[0] <= 800
            assert img.size[1] <= 600
