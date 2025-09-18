import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestSortProductByName:
    def test_sort_products_by_name_ascending(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Banana", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Apple", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Cherry", description="Description3", price=45.00, stock_quantity=4, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "name"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        returned_product_names = [product["name"] for product in response.data['results']]
        assert returned_product_names == ["Apple", "Banana", "Cherry"]

    def test_sort_products_by_name_descending(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Banana", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Apple", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Cherry", description="Description3", price=45.00, stock_quantity=4, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "-name"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        returned_product_names = [product["name"] for product in response.data['results']]
        assert returned_product_names == ["Cherry", "Banana", "Apple"]

    def test_sort_products_by_name_with_identical_names(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Apple", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Apple", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Banana", description="Description3", price=45.00, stock_quantity=4, category=category)
        product4 = product_factory(name="Banana", description="Description4", price=25.00, stock_quantity=5, category=category)
        product5 = product_factory(name="Cherry", description="Description5", price=15.00, stock_quantity=6, category=category)
        product6 = product_factory(name="Cherry", description="Description6", price=35.00, stock_quantity=3, category=category)
        product7 = product_factory(name="Date", description="Description7", price=40.00, stock_quantity=2, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "name"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 7
        returned_product_names = [product["name"] for product in response.data['results']]
        assert returned_product_names == ["Apple", "Apple", "Banana", "Banana", "Cherry", "Cherry", "Date"]

@pytest.mark.django_db
class TestSortProductByPrice:
    def test_sort_products_by_price_ascending(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Product 1", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Product 2", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Product 3", description="Description3", price=45.00, stock_quantity=4, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "price"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        returned_product_prices = [product["price"] for product in response.data['results']]
        assert returned_product_prices == ['20.00', '30.00', '45.00']

    def test_sort_products_by_price_descending(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Product 1", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Product 2", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Product 3", description="Description3", price=45.00, stock_quantity=4, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "-price"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        returned_product_prices = [product["price"] for product in response.data['results']]
        assert returned_product_prices == ['45.00', '30.00', '20.00']

    def test_sort_products_by_price_with_identical_prices(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Product 1", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Product 2", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Product 3", description="Description3", price=30.00, stock_quantity=4, category=category)
        product4 = product_factory(name="Product 4", description="Description4", price=20.00, stock_quantity=5, category=category)
        product5 = product_factory(name="Product 5", description="Description5", price=45.00, stock_quantity=6, category=category)
        product6 = product_factory(name="Product 6", description="Description6", price=45.00, stock_quantity=3, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "price"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 6
        returned_product_prices = [product["price"] for product in response.data['results']]
        assert returned_product_prices == ['20.00', '20.00', '30.00', '30.00', '45.00', '45.00']


@pytest.mark.django_db
class TestSortProductByCreatedAt:
    def test_sort_products_by_created_at_ascending(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Product 1", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Product 2", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Product 3", description="Description3", price=45.00, stock_quantity=4, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "created_at"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        returned_product_names = [product["name"] for product in response.data['results']]
        assert returned_product_names == ["Product 1", "Product 2", "Product 3"]

    def test_sort_products_by_created_at_descending(self, api_client, product_factory, category_factory):
        category = category_factory(name="Category 1")
        product1 = product_factory(name="Product 1", description="Description1", price=30.00, stock_quantity=8, category=category)
        product2 = product_factory(name="Product 2", description="Description2", price=20.00, stock_quantity=7, category=category)
        product3 = product_factory(name="Product 3", description="Description3", price=45.00, stock_quantity=4, category=category)

        url = reverse("catalog:product-list")
        response = api_client.get(url, {"ordering": "-created_at"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        returned_product_names = [product["name"] for product in response.data['results']]
        assert returned_product_names == ["Product 3", "Product 2", "Product 1"]
