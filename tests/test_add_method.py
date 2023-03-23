import pytest

import allure
from common.checkers import check_failure_reason_no_required_field
from common.checkers import check_failure_reason_wrong_data_type
from common.checkers import check_failure_reason_wrong_param_data_type
from common.constants import ADD_UPDATE_REQUIRED_PARAMS
from common.constants import INT_INCORRECT_DATA_TYPES
from common.constants import INT_PARAMS
from common.constants import STRING_ADD_UPDATE_PARAMS
from common.constants import STRING_INCORRECT_DATA_TYPES
from common.constants import WRONG_DATA_TYPES
from common.helpers import run
from schemas.response import AddResponse
from schemas.response import FailureResponse


@allure.epic("Добавление нового юзера")
@allure.feature("Успешное добавление нового юзера")
@allure.story("Успешное добавление нового юзера")
def test_success_add_user(create_add_request, client):
    response = run(client.send_message_success(create_add_request))

    AddResponse(**response)


@allure.epic("Добавление нового юзера")
@allure.feature("Успешное добавление нового юзера")
@allure.story("Успешное добавление нового юзера с отличающимся телефоном")
def test_success_add_user_different_phone(create_add_request, client):
    run(client.send_message_success(create_add_request))
    phone = int(create_add_request["phone"])
    phone += 1
    create_add_request["phone"] = str(phone)
    response = run(client.send_message_success(create_add_request))

    AddResponse(**response)


@allure.epic("Добавление нового юзера")
@allure.feature("Добавление нового юзера с ошибкой")
@allure.story("Добавление уже существующего юзера")
def test_failure_add_user_duplicate_user(create_add_request, client):
    run(client.send_message_success(create_add_request))
    response = run(client.send_message_failure(create_add_request))

    FailureResponse(**response)


@allure.epic("Добавление нового юзера")
@allure.feature("Добавление нового юзера с ошибкой")
@allure.story("В запросе отсутствуют обязательные поля")
@pytest.mark.parametrize("req_param", [*ADD_UPDATE_REQUIRED_PARAMS])
def test_failure_add_user_no_required_fields(create_add_request, client, req_param):
    data = create_add_request
    data.pop(req_param)
    response = run(client.send_message_failure(data))

    FailureResponse(**response)
    check_failure_reason_no_required_field(response, req_param)


@allure.epic("Добавление нового юзера")
@allure.feature("Добавление нового юзера с ошибкой")
@allure.story("Запрос имеет некорректный тип данных")
@pytest.mark.parametrize("param", [*WRONG_DATA_TYPES])
def test_failure_add_user_wrong_structure(client, param):
    response = run(client.send_message_failure(data=param))

    FailureResponse(**response)
    check_failure_reason_wrong_data_type(response)


@allure.epic("Добавление нового юзера")
@allure.feature("Добавление нового юзера с ошибкой")
@allure.story("Строковые поля запроса имеют некорректный тип данных")
@pytest.mark.parametrize("param", [*STRING_ADD_UPDATE_PARAMS])
@pytest.mark.parametrize("wrong_type", [*STRING_INCORRECT_DATA_TYPES])
def test_failure_add_user_wrong_type_str_fields(client, create_add_request, param, wrong_type):
    create_add_request[param] = wrong_type
    response = run(client.send_message_failure(create_add_request))

    FailureResponse(**response)
    check_failure_reason_wrong_param_data_type(response)


@allure.epic("Добавление нового юзера")
@allure.feature("Добавление нового юзера с ошибкой")
@allure.story("Числовые поля запроса имеют некорректный тип данных")
@pytest.mark.parametrize("param", [*INT_PARAMS])
@pytest.mark.parametrize("wrong_type", [*INT_INCORRECT_DATA_TYPES])
def test_failure_add_user_wrong_type_int_fields(client, create_add_request, param, wrong_type):
    create_add_request[param] = wrong_type
    response = run(client.send_message_failure(create_add_request))

    FailureResponse(**response)
    check_failure_reason_wrong_param_data_type(response)
