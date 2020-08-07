from django.urls import reverse
import pytest
from ..models import AppStoreReview


@pytest.fixture
def function_fixture():
    print("Fixture for each test")
    return 1


TEST_SIZE = 10


@pytest.fixture
def appstorereview():
    return AppStoreReview.objects.create(
        author="PytestBot",
        version=0.0,
        rating=3,
        title="from the console!",
        content="well played",
        country="uk",
        app_id=6,
    )


class TestTask:
    def test_create_appstorereviews(self, admin_client, appstorereview):
        test_url = reverse(
            "itunes-review-list-create", kwargs={"int": appstorereview.id,}
        )

        for i in range(TEST_SIZE):
            response = client.post(
                test_url,
                data =  
            )

