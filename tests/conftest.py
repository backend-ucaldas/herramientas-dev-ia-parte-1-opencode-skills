import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "DATABASE_URL": "sqlite://"})
    with app.test_client() as client:
        yield client
