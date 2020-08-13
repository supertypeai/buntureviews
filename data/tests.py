from django.test import TestCase
from user.models import User
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from .models import *
from .api.serializers import *
import json
# Create your tests here.

TEST_DATA = """
{
    "author": "Md Nazmul Hasan",
    "version": "0.0.1",
    "rating": 4,
    "title": "Test App title",
    "content": "test content",
    "country": "gb",
    "app": 1
}
"""

APP_DATA = """
{
    "appid": "echo.co.uk",
    "primaryCountry": "gb"
}
"""

class AppStoreReviewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_model = User
        self.user = user_model.objects.create_user(
            username="yin", password="1233456")
        
    
    def create_app(self):
        self.client.force_authenticate(user=self.user)
        create_app_url = "/api/app"
        app_response = self.client.post(create_app_url, json.loads(APP_DATA), format="json")
        self.assertEqual(app_response.status_code, 201)
        self.client.logout()
        
        
    
    def test_app_review_bulk_creation(self):
        self.client.force_authenticate(user=self.user)
        app_instacne = App.objects.create(**json.loads(APP_DATA))

        app_review_data = json.loads(TEST_DATA)
        app_review_data["app"] = app_instacne.id

        reviews = [app_review_data for i in range(1,600)]

        data = {"reviews": reviews}
        url = "/api/reviews/appstore/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        self.client.logout()


