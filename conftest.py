import pytest

from common.helpers import Client

pytest_plugins = [
    "fixtures.fixtures",
]


@pytest.fixture(scope="session")
def client():
    return Client()
