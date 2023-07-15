import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_not_authenticate_returns_401(self):
        client = APIClient()
        response = client.post("/store/collections/", {"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post("/store/collections/", {"title": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post("/store/collections/", {"title": ""})

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert response.data["title"] is not None