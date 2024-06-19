from faker import Faker

from tests.utils.logger import configure_logging

import pytest

from tests.utils.http_client import HttpClient


configure_logging()
BASE_URL = 'http://localhost:8000/api/'


@pytest.fixture(scope="session")
def http_client():
    client = HttpClient(BASE_URL)
    client.headers["Content-Type"] = "application/vnd.api+json"
    yield client


@pytest.fixture
def fake_data():
    yield Faker()
