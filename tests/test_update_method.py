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
from schemas.response import FailureResponse
from schemas.response import UpdateResponse
from schemas.response import UpdateResponseFailure


@allure.epic("Обновление данных юзера")
@allure.feature("Успешное обновление данных юзера")
@allure.story("Успешное обновление данных юзера")
def test_success_update_user(create_user, create_update_request, client):
    create_update_request['phone'] = create_user['phone']
    response = run(client.send_message_success(create_update_request))

    UpdateResponse(**response)


@allure.epic("Обновление данных юзера")
@allure.feature("Обновление данных юзера с ошибкой")
@allure.story("Обновление не существующего юзера")
def test_failure_update_user_not_found(create_update_request, client):
    response = run(client.send_message_failure(create_update_request))

    UpdateResponseFailure(**response)


@allure.epic("Обновление данных юзера")
@allure.feature("Обновление данных юзера с ошибкой")
@allure.story("В запросе отсутствуют обязательные поля")
@pytest.mark.parametrize("req_param", [*ADD_UPDATE_REQUIRED_PARAMS])
def test_failure_update_user_no_required_fields(create_update_request, client, req_param):
    data = create_update_request
    data.pop(req_param)
    response = run(client.send_message_failure(data))

    FailureResponse(**response)
    check_failure_reason_no_required_field(response, req_param)


@allure.epic("Обновление данных юзера")
@allure.feature("Обновление данных юзера с ошибкой")
@allure.story("Запрос имеет некорректный тип данных")
@pytest.mark.parametrize("param", [*WRONG_DATA_TYPES])
def test_failure_update_user_wrong_structure(client, param):
    response = run(client.send_message_failure(data=param))

    FailureResponse(**response)
    check_failure_reason_wrong_data_type(response)


@allure.epic("Обновление данных юзера")
@allure.feature("Обновление данных юзера с ошибкой")
@allure.story("Строковые поля запроса имеют некорректный тип данных")
@pytest.mark.parametrize("param", [*STRING_ADD_UPDATE_PARAMS])
@pytest.mark.parametrize("wrong_type", [*STRING_INCORRECT_DATA_TYPES])
def test_failure_update_user_wrong_type_str_fields(client, create_update_request, param, wrong_type):
    create_update_request[param] = wrong_type
    response = run(client.send_message_failure(create_update_request))

    FailureResponse(**response)
    check_failure_reason_wrong_param_data_type(response)


@allure.epic("Обновление данных юзера")
@allure.feature("Обновление данных юзера с ошибкой")
@allure.story("Числовые поля запроса имеют некорректный тип данных")
@pytest.mark.parametrize("param", [*INT_PARAMS])
@pytest.mark.parametrize("wrong_type", [*INT_INCORRECT_DATA_TYPES])
def test_failure_update_user_wrong_type_int_fields(client, create_update_request, param, wrong_type):
    create_update_request[param] = wrong_type
    response = run(client.send_message_failure(create_update_request))

    FailureResponse(**response)
    check_failure_reason_wrong_param_data_type(response)


@allure.epic("Обновление данных юзера")
@allure.feature("Обновление данных юзера с ошибкой")
@allure.story("Неудачная попытка SQL инъекции")
def test_failure_update_injection(create_user, create_update_request, client):
    pattern = "1' or '1' = '1"
    create_update_request["name"] = pattern
    response = run(client.send_message_failure(create_update_request))

    UpdateResponseFailure(**response)
    assert len(response['users']) == 0
