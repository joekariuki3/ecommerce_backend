import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductViewSet:
    def test_create_product_as_anonymous(self, api_client):
        url = reverse("catalog:product-list")
        data = {"name": "New Product"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_product_as_non_admin(self, api_client, default_user):
        api_client.force_authenticate(user=default_user)
        url = reverse("catalog:product-list")
        data = {"name": "New Product"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product_as_admin(
        self, admin_authenticated_client, category_factory
    ):
        category = category_factory(name="Electronics")
        url = reverse("catalog:product-list")
        data = {
            "name": "New Product",
            "description": "A great product",
            "price": "99.99",
            "stock_quantity": 10,
            "category_id": category.id,
        }
        response = admin_authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Product"
        assert response.data["category"]["name"] == "Electronics"

        # Test that the product is associated with the category
        url = reverse("catalog:product-detail", kwargs={"pk": response.data["id"]})
        response = admin_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["category"]["name"] == "Electronics"
        assert response.data["category"]["description"] is None
        assert response.data["category"]["id"] == str(category.id)
        assert response.data["name"] == "New Product"
        assert response.data["description"] == "A great product"
        assert response.data["price"] == "99.99"
        assert response.data["stock_quantity"] == 10

    def test_create_product_with_invalid_data_as_admin(
        self, admin_authenticated_client, category_factory
    ):
        category = category_factory(name="Electronics")
        url = reverse("catalog:product-list")
        data = {
            "name": "",  # Invalid: name is required
            "description": "A great product",
            "price": -10.0,  # Invalid: price must be non-negative
            "stock_quantity": -5,  # Invalid: stock_quantity must be non-negative
            "category_id": category.id,
        }
        response = admin_authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert "price" in response.data
        assert "stock_quantity" in response.data

    def test_create_product_with_nonexistent_category_as_admin(
        self, admin_authenticated_client
    ):
        url = reverse("catalog:product-list")
        data = {
            "name": "New Product",
            "description": "A great product",
            "price": "99.99",
            "stock_quantity": 10,
            "category_id": "nonexistent-id",
        }
        response = admin_authenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category_id" in response.data
        assert response.data["category_id"][0].code == "invalid"

    def test_list_products(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product_factory(
            name="Product 1",
            description="Description 1",
            price=10.0,
            stock_quantity=5,
            category_id=category.id,
        )
        product_factory(
            name="Product 2",
            description="Description 2",
            price=20.0,
            stock_quantity=15,
            category_id=category.id,
        )
        url = reverse("catalog:product-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        product_names = {product["name"] for product in response.data["results"]}
        assert "Product 1" in product_names
        assert "Product 2" in product_names

    def test_list_products_empty(self, api_client):
        url = reverse("catalog:product-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"] == []

    def test_retrieve_product(self, api_client, product_factory, category_factory):
        category = category_factory(name="Electronics")
        product = product_factory(
            name="Product 1",
            description="Description 1",
            price=10.0,
            stock_quantity=5,
            category_id=category.id,
        )
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Product 1"
        assert response.data["id"] == str(product.id)

    def test_retrieve_nonexistent_product(self, api_client):
        url = reverse("catalog:product-detail", kwargs={"pk": "nonexistent-id"})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"].code == "not_found"

    def test_update_product_as_admin(
        self, admin_authenticated_client, product_factory, category_factory
    ):
        category = category_factory(name="Old Category")
        product = product_factory(
            name="Old Product",
            description="Old description",
            price=50.0,
            stock_quantity=10,
            category_id=category.id,
        )
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        new_category = category_factory(name="New Category")
        data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 199.99,
            "stock_quantity": 5,
            "category_id": new_category.id,
        }
        response = admin_authenticated_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Product"
        assert response.data["category"]["name"] == "New Category"

    def test_update_product_as_non_admin(
        self, api_client, default_user, product_factory, category_factory
    ):
        category = category_factory(name="Electronics")
        product = product_factory(
            name="Product 1",
            description="Description 1",
            price=10.0,
            stock_quantity=5,
            category_id=category.id,
        )
        api_client.force_authenticate(user=default_user)
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 199.99,
            "stock_quantity": 5,
            "category_id": category.id,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"].code == "permission_denied"

    def test_partial_update_product_as_admin(
        self, admin_authenticated_client, product_factory, category_factory
    ):
        category = category_factory(name="Old Category")
        product = product_factory(
            name="Old Product",
            description="Old description",
            price=50.0,
            stock_quantity=10,
            category_id=category.id,
        )
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        new_category = category_factory(name="New Category")
        data = {
            "name": "Partially Updated Product",
            "category_id": new_category.id,
        }
        response = admin_authenticated_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Partially Updated Product"
        assert response.data["category"]["name"] == "New Category"
        assert response.data["description"] == "Old description"
        assert response.data["price"] == "50.00"
        assert response.data["stock_quantity"] == 10

    def test_partial_update_product_as_non_admin(
        self, api_client, default_user, product_factory, category_factory
    ):
        category = category_factory(name="Electronics")
        product = product_factory(
            name="Product 1",
            description="Description 1",
            price=10.0,
            stock_quantity=5,
            category_id=category.id,
        )
        api_client.force_authenticate(user=default_user)
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        data = {
            "name": "Partially Updated Product",
        }
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"].code == "permission_denied"

        # Verify the product is unchanged
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Product 1"

    def test_partial_update_product_with_nonexistent_category_as_admin(
        self, admin_authenticated_client, product_factory, category_factory
    ):
        category = category_factory(name="Electronics")
        product = product_factory(
            name="Product 1",
            description="Description 1",
            price=10.0,
            stock_quantity=5,
            category_id=category.id,
        )
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        data = {
            "category_id": "nonexistent-id",
        }
        response = admin_authenticated_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category_id" in response.data
        assert response.data["category_id"][0].code == "invalid"

    def test_delete_product_as_admin(
        self, admin_authenticated_client, product_factory, category_factory
    ):
        category = category_factory(name="Electronics")
        product = product_factory(
            name="Product to Delete",
            description="Description",
            price=30.0,
            stock_quantity=8,
            category_id=category.id,
        )
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        response = admin_authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify the product is deleted
        response = admin_authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_as_non_admin(
        self, api_client, default_user, product_factory, category_factory
    ):
        category = category_factory(name="Electronics")
        product = product_factory(
            name="Product to Delete",
            description="Description",
            price=30.0,
            stock_quantity=8,
            category_id=category.id,
        )
        api_client.force_authenticate(user=default_user)
        url = reverse("catalog:product-detail", kwargs={"pk": product.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"].code == "permission_denied"

        # Verify the product still exists
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
