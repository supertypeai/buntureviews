from django.urls import reverse
import pytest
from ..models import AppStoreReview


# TEST_SIZE = 10

# this is not actually executed, it's just a fixture
# @pytest.fixture
# def appstorereview():
#     return AppStoreReview.objects.create(
#         author="PytestBot",
#         version=0.0,
#         rating=3,
#         title="from the console!",
#         content="well played",
#         country="uk",
#         app_id=6,
#     )


# class TestTask:
#     def test_create_appstorereviews(self, admin_client, appstorereview):
#         test_url = reverse(
#             "itunes-review-list-create", kwargs={"int": appstorereview.id,}
#         )

#         for i in range(TEST_SIZE):
#             response = client.post(test_url, data=2)

