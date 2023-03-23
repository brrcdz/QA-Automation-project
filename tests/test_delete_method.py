import pytest

import allure
from common.checkers import check_failure_reason_no_required_field
from common.checkers import check_failure_reason_wrong_data_type
from common.checkers import check_failure_reason_wrong_param_data_type
from common.constants import DELETE_REQUIRED_PARAMS
from common.constants import STRING_DELETE_PARAMS
from common.constants import STRING_INCORRECT_DATA_TYPES
from common.constants import WRONG_DATA_TYPES
from common.helpers import run
from schemas.response import DeleteResponse
from schemas.response import FailureResponse


@allure.epic("Удаление юзера")
@allure.feature("Успешное удаление юзера")
@allure.story("Успешное удаление юзера")
def test_success_delete_user(create_delete_request, client, create_user):
    create_delete_request["phone"] = create_user["phone"]
    response = run(client.send_message_success(create_delete_request))

    DeleteResponse(**response)


@allure.epic("Удаление юзера")
@allure.feature("Удаление юзера с ошибкой")
@allure.story("Удаление несуществующего юзера")
def test_failure_delete_user_not_found(create_delete_request, client):
    response = run(client.send_message_failure(create_delete_request))

    FailureResponse(**response)


@allure.epic("Удаление юзера")
@allure.feature("Удаление юзера с ошибкой")
@allure.story("В запросе отсутствует обязательное поле")
@pytest.mark.parametrize("req_param", [*DELETE_REQUIRED_PARAMS])
def test_failure_delete_user_no_required_fields(create_delete_request, client, req_param):
    data = create_delete_request
    data.pop(req_param)
    response = run(client.send_message_failure(data))

    FailureResponse(**response)
    check_failure_reason_no_required_field(response, req_param)


@allure.epic("Удаление юзера")
@allure.feature("Удаление юзера с ошибкой")
@allure.story("Запрос имеет некорректный тип данных")
@pytest.mark.parametrize("param", [*WRONG_DATA_TYPES])
def test_failure_delete_user_wrong_structure(client, param):
    response = run(client.send_message_failure(data=param))

    FailureResponse(**response)
    check_failure_reason_wrong_data_type(response)


@allure.epic("Удаление юзера")
@allure.feature("Удаление юзера с ошибкой")
@allure.story("Поля запроса имеют некорректный тип данных")
@pytest.mark.parametrize("param", [*STRING_DELETE_PARAMS])
@pytest.mark.parametrize("wrong_type", [*STRING_INCORRECT_DATA_TYPES])
def test_failure_delete_user_wrong_fields_type(client, create_delete_request, param, wrong_type):
    create_delete_request[param] = wrong_type
    response = run(client.send_message_failure(create_delete_request))

    FailureResponse(**response)
    check_failure_reason_wrong_param_data_type(response)


def test_failure_injection():
    pass
