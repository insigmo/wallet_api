import pytest
from faker import Faker

from utils.http_client import HttpClient
from utils.logger import configure_logging

configure_logging()
BASE_URL = 'http://web:8000/api/'


@pytest.fixture(scope="session")
def http_client():
    client = HttpClient(BASE_URL)
    client.headers["Content-Type"] = "application/vnd.api+json"
    yield client


@pytest.fixture
def fake_data():
    yield Faker()
