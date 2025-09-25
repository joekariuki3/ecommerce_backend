import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_category_as_admin(admin_authenticated_client):
    url = reverse("catalog:category-list")
    data = {"name": "New Category"}
    response = admin_authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "New Category"


@pytest.mark.django_db
def test_create_category_as_non_admin(authenticated_client_and_user):
    client, _ = authenticated_client_and_user
    url = reverse("catalog:category-list")
    data = {"name": "New Category"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_category_as_anonymous(api_client):
    url = reverse("catalog:category-list")
    data = {"name": "New Category"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_category_without_name_as_admin(admin_authenticated_client):
    url = reverse("catalog:category-list")
    data = {"description": "A category without a name"}
    response = admin_authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert response.data["name"][0].code == "required"
    assert response.data["name"][0] == "This field is required."


@pytest.mark.django_db
def test_create_category_with_blank_description_as_admin(admin_authenticated_client):
    url = reverse("catalog:category-list")
    data = {"name": "Category with Blank Description", "description": ""}
    response = admin_authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Category with Blank Description"
    assert response.data["description"] == ""
    assert response.data["id"] is not None


@pytest.mark.django_db
def test_create_duplicate_category_name(admin_authenticated_client, category_factory):
    category_factory(name="Unique Category")
    url = reverse("catalog:category-list")
    data = {"name": "Unique Category"}
    response = admin_authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert response.data["name"][0].code == "unique"
    assert response.data["name"][0] == "category with this name already exists."


@pytest.mark.django_db
def test_list_categories_as_anonymous(api_client, category_factory):
    category_factory(name="Category 1")
    category_factory(name="Category 2")
    url = reverse("catalog:category-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Category 1"
    assert response.data[1]["name"] == "Category 2"


@pytest.mark.django_db
def test_retrieve_category_as_anonymous(api_client, category_factory):
    category = category_factory(name="Category 1")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Category 1"


@pytest.mark.django_db
def test_retrieve_nonexistent_category(api_client):
    url = reverse("catalog:category-detail", kwargs={"pk": 9999})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_category_as_admin(admin_authenticated_client, category_factory):
    category = category_factory(name="Old Name")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    data = {"name": "Updated Name"}
    response = admin_authenticated_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Name"
    category.refresh_from_db()
    assert category.name == "Updated Name"


@pytest.mark.django_db
def test_update_category_as_non_admin(authenticated_client_and_user, category_factory):
    client, _ = authenticated_client_and_user
    category = category_factory(name="Old Name")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    data = {"name": "Updated Name"}
    response = client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    category.refresh_from_db()
    assert category.name == "Old Name"


@pytest.mark.django_db
def test_update_category_as_anonymous(api_client, category_factory):
    category = category_factory(name="Old Name")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    data = {"name": "Updated Name"}
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    category.refresh_from_db()
    assert category.name == "Old Name"


@pytest.mark.django_db
def test_partial_update_category_as_admin(admin_authenticated_client, category_factory):
    category = category_factory(name="Initial Name", description="Initial Description")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    data = {"description": "Partially Updated Description"}
    response = admin_authenticated_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Initial Name"
    assert response.data["description"] == "Partially Updated Description"
    category.refresh_from_db()
    assert category.name == "Initial Name"
    assert category.description == "Partially Updated Description"


@pytest.mark.django_db
def test_partial_update_category_as_non_admin(
    authenticated_client_and_user, category_factory
):
    client, _ = authenticated_client_and_user
    category = category_factory(name="Initial Name", description="Initial Description")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    data = {"description": "Partially Updated Description"}
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    category.refresh_from_db()
    assert category.name == "Initial Name"
    assert category.description == "Initial Description"


@pytest.mark.django_db
def test_partial_update_category_as_anonymous(api_client, category_factory):
    category = category_factory(name="Initial Name", description="Initial Description")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    data = {"description": "Partially Updated Description"}
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    category.refresh_from_db()
    assert category.name == "Initial Name"
    assert category.description == "Initial Description"


@pytest.mark.django_db
def test_delete_category_as_admin(admin_authenticated_client, category_factory):
    category = category_factory(name="To Be Deleted")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    response = admin_authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not category.__class__.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_delete_category_as_non_admin(authenticated_client_and_user, category_factory):
    client, _ = authenticated_client_and_user
    category = category_factory(name="To Be Deleted")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert category.__class__.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_delete_category_as_anonymous(api_client, category_factory):
    category = category_factory(name="To Be Deleted")
    url = reverse("catalog:category-detail", kwargs={"pk": category.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert category.__class__.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_create_category_with_long_name(admin_authenticated_client):
    url = reverse("catalog:category-list")
    long_name = "A" * 300
    data = {"name": long_name}
    response = admin_authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert response.data["name"][0].code == "max_length"
    assert (
        response.data["name"][0] == "Ensure this field has no more than 255 characters."
    )
