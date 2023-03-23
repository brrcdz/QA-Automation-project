import pytest

from schemas.schema import GeneratedAddBody
from schemas.schema import GeneratedDeleteBody
from schemas.schema import GeneratedSelectBody
from schemas.schema import GeneratedUpdateBody


@pytest.fixture
def create_add_request():
    return GeneratedAddBody.build().dict()


@pytest.fixture
def create_add_requests():
    return GeneratedAddBody.batch(3)


@pytest.fixture
def create_user(client, create_add_request):
    client.send_message_success(create_add_request)
    return create_add_request


@pytest.fixture
def create_multiple_users(client, create_add_requests):
    users = [user.dict() for user in create_add_requests]
    for user in users:
        user["name"] = "Foo"
        user["surname"] = "Bar"
        client.send_message_success(user)
    return users


@pytest.fixture
def create_delete_request():
    return GeneratedDeleteBody.build().dict()


@pytest.fixture
def create_select_request():
    return GeneratedSelectBody.build().dict()


@pytest.fixture
def create_select_by_phone_request(create_select_request):
    create_select_request.pop("name")
    create_select_request.pop("surname")
    return create_select_request


@pytest.fixture
def create_select_by_name_request(create_select_request):
    create_select_request.pop("phone")
    create_select_request.pop("surname")
    return create_select_request


@pytest.fixture
def create_select_by_surname_request(create_select_request):
    create_select_request.pop("name")
    create_select_request.pop("phone")
    return create_select_request


@pytest.fixture
def create_update_request():
    return GeneratedUpdateBody.build().dict()
