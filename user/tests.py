import pytest
from user.models import User

# Create your tests here.
@pytest.mark.django_db
def test_user_create():
    User(username="test_username", email="test@mail.com").save()
    assert User.objects.count() == 1
