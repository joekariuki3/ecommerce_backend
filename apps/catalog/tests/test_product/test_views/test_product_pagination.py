import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductPagination:
    def test_product_pagination_default(self, api_client, create_products):
        create_products(25)

        product_list_url = reverse("catalog:product-list")
        response = api_client.get(product_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 10  # Default page size is 10
        assert response.data["count"] == 25
        assert response.data["next"] is not None
        assert response.data["previous"] is None

    def test_product_pagination_custom_page_size(self, api_client, create_products):
        create_products(25)

        product_list_url = reverse("catalog:product-list")
        response = api_client.get(product_list_url, {"page_size": 15})
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 15  # Custom page size is 15
        assert response.data["count"] == 25
        assert response.data["next"] is not None
        assert response.data["previous"] is None

        # Requesting page 2
        response = api_client.get(product_list_url, {"page": 2, "page_size": 15})
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 10  # Remaining products on page 2
        assert response.data["count"] == 25
        assert response.data["next"] is None
        assert response.data["previous"] is not None

    def test_product_pagination_exceed_max_page_size(self, api_client, create_products):
        create_products(25)

        product_list_url = reverse("catalog:product-list")
        response = api_client.get(product_list_url, {"page_size": 150})
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 25  # Only 25 products available
        assert response.data["count"] == 25
        assert response.data["next"] is None
        assert response.data["previous"] is None

        # Requesting page 2 should return 404 as there is no page 2
        response = api_client.get(product_list_url, {"page": 2, "page_size": 150})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Invalid page."
        assert "results" not in response.data

    def test_product_pagination_invalid_page(self, api_client, create_products):
        create_products(25)

        product_list_url = reverse("catalog:product-list")
        response = api_client.get(product_list_url, {"page": 0})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Invalid page."
        assert "results" not in response.data

        response = api_client.get(product_list_url, {"page": -1})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Invalid page."
        assert "results" not in response.data

        response = api_client.get(product_list_url, {"page": 100})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Invalid page."
        assert "results" not in response.data
