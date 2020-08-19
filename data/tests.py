from django.urls import reverse
from user.models import User
import pytest
import json, logging

logger = logging.getLogger(__name__)

# Create your tests here.
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def admin_user(db, django_user_model):
    username = "test_admin"
    email = "test@admin.com"
    password = "demo123*56"
    user = django_user_model.objects.create(
        username=username, email=email, is_superuser=True, is_staff=True
    )
    user.set_password(password)
    user.save()
    return user


@pytest.mark.django_db
def test_customer_url(api_client):
    url = reverse("customer-create")
    response = api_client.get(url)
    assert response.status_code == 405


@pytest.mark.django_db
def test_customer_creation(api_client):
    url = reverse("customer-create")
    data = {
        "user": {"username": "devadmin2", "email": "devadmin2@test.com"},
        "accountName": "testAccountName",
    }
    if User.objects.filter(username=data["user"]["username"]).exists() == True:
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 400
    else:
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 201

    data2 = {
        "user": {"username": "devadmin23", "email": "devadmin23@test.com"},
        "accountName": "",
    }
    response = api_client.post(url, data=data2, format="json")
    assert response.status_code == 400

    data3 = {
        "user": {"username": "devadmin23", "email": "devadmin23@test.com"},
        "accountName": None,
    }
    response = api_client.post(url, data=data2, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_app_list_authorization(api_client, admin_user):
    url = reverse("app-list-create")
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.force_authenticate(user=admin_user)
    response = api_client.get(url)
    assert response.status_code == 200
    api_client.logout()
