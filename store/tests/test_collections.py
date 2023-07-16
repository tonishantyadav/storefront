import pytest
from rest_framework import status
from model_bakery import baker

from store import models


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_not_authenticate_returns_401(self, create_collection):
        response = create_collection({"title": "a"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticate_user, create_collection
    ):
        authenticate_user()
        response = create_collection({"title": "a"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate_user, create_collection):
        authenticate_user(is_staff=True)
        response = create_collection({"title": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(self, authenticate_user, create_collection):
        authenticate_user(is_staff=True)
        response = create_collection({"title": "a"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetriveCollection:
    def test_if_collections_exists_returns_200(self, api_client):
        collection = baker.make(models.Collection)
        response = api_client.get(f"/store/collections/{collection.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count": 0,
        }
