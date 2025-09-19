import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductSearchByName:
    def test_search_product_by_name(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)
        product_factory(name="Google Pixel 6", price=599.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "iPhone"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Apple iPhone 13"

    def test_search_product_by_partial_name(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)
        product_factory(name="Google Pixel 6", price=599.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "Galaxy"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Samsung Galaxy S21"

    def test_search_product_no_results(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)
        product_factory(name="Google Pixel 6", price=599.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "Nokia"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_search_product_case_insensitive(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)
        product_factory(name="Google Pixel 6", price=599.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "iphone"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Apple iPhone 13"

    def test_search_product_multiple_results(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Apple MacBook Pro", price=1299.99, category_id=category.id)
        product_factory(name="Apple AirPods Pro", price=249.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "Apple"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3
        product_names = [product["name"] for product in response.data["results"]]
        assert "Apple iPhone 13" in product_names
        assert "Apple MacBook Pro" in product_names
        assert "Apple AirPods Pro" in product_names

    def test_search_product_special_characters(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Sony WH-1000XM4", price=349.99, category_id=category.id)
        product_factory(name="Bose QuietComfort 35 II", price=299.99, category_id=category.id)
        product_factory(name="Apple AirPods Pro", price=249.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "WH-1000XM4"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Sony WH-1000XM4"

    def test_search_product_empty_query(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": ""})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        product_names = [product["name"] for product in response.data["results"]]
        assert "Apple iPhone 13" in product_names
        assert "Samsung Galaxy S21" in product_names

    def test_search_product_whitespace_query(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="Apple iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "   "})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        product_names = [product["name"] for product in response.data["results"]]
        assert "Apple iPhone 13" in product_names
        assert "Samsung Galaxy S21" in product_names

    def test_search_product_numeric_query(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(name="iPhone 13", price=999.99, category_id=category.id)
        product_factory(name="Samsung Galaxy S21", price=799.99, category_id=category.id)
        product_factory(name="Pixel 6", price=599.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "13"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "iPhone 13"

    def test_search_product_unicode_query(self, api_client, product_factory, category_factory):
        category = category_factory(name="Books")
        product_factory(name="Cien años de soledad", price=19.99, category_id=category.id)
        product_factory(name="Les Misérables", price=14.99, category_id=category.id)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"search": "años"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Cien años de soledad"

        response = api_client.get(url, {"search": "Misé"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Les Misérables"

    def test_search_product_long_query(self, api_client, product_factory, category_factory):
        category = category_factory(name="Books")
        product_factory(name="A very long book title that exceeds normal length", price=29.99, category_id=category.id)
        product_factory(name="Short Title", price=9.99, category_id=category.id)

        url = reverse("catalog:product-list")
        long_query = "A very long book title that exceeds normal length"
        response = api_client.get(url, {"search": long_query})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "A very long book title that exceeds normal length"