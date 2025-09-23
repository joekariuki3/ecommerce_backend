import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestFilterProductByCategory:
    def test_filter_products_by_category(
        self, api_client, product_factory, category_factory
    ):
        category1 = category_factory(name="Category 1")
        category2 = category_factory(name="Category 2")
        product_factory(
            name="Product 1",
            description="Description1",
            price=30.0,
            stock_quantity=8,
            category=category1,
        )
        product_factory(
            name="Product 2",
            description="Description2",
            price=20.0,
            stock_quantity=7,
            category=category2,
        )
        product_factory(
            name="Product 3",
            description="Description3",
            price=45.0,
            stock_quantity=4,
            category=category1,
        )

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"category__id": category1.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        returned_product_names = {
            product["name"] for product in response.data["results"]
        }
        assert returned_product_names == {"Product 1", "Product 3"}

    def test_filter_products_by_nonexistent_category(
        self, api_client, product_factory, category_factory
    ):
        category1 = category_factory(name="Category 1")
        category2 = category_factory(name="Category 2")
        product_factory(
            name="Product 1",
            description="Description1",
            price=30.0,
            stock_quantity=8,
            category=category1,
        )
        product_factory(
            name="Product 2",
            description="Description2",
            price=20.0,
            stock_quantity=7,
            category=category2,
        )

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"category__id": "nonexistent-id"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category__id" in response.data
        assert response.data["category__id"][0].code == "invalid"

    def test_filter_products_by_category_no_matches(
        self, api_client, product_factory, category_factory
    ):
        category1 = category_factory(name="Category 1")
        category2 = category_factory(name="Category 2")
        category3 = category_factory(name="Category 3")
        product_factory(
            name="Product 1",
            description="Description1",
            price=30.0,
            stock_quantity=8,
            category=category1,
        )
        product_factory(
            name="Product 2",
            description="Description2",
            price=20.0,
            stock_quantity=7,
            category=category2,
        )

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"category__id": category3.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_filter_products_without_category_param(
        self, api_client, product_factory, category_factory
    ):
        category1 = category_factory(name="Category 1")
        category2 = category_factory(name="Category 2")
        product_factory(
            name="Product 1",
            description="Description1",
            price=30.0,
            stock_quantity=8,
            category=category1,
        )
        product_factory(
            name="Product 2",
            description="Description2",
            price=20.0,
            stock_quantity=7,
            category=category2,
        )

        url = reverse("catalog:product-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        returned_product_names = {
            product["name"] for product in response.data["results"]
        }
        assert returned_product_names == {"Product 1", "Product 2"}
