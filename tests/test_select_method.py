import pytest

import allure
from common.checkers import check_failure_reason_no_required_field
from common.checkers import check_failure_reason_wrong_data_type
from common.checkers import check_failure_reason_wrong_param_data_type
from common.checkers import check_users
from common.constants import SELECT_REQUIRED_PARAMS
from common.constants import STRING_INCORRECT_DATA_TYPES
from common.constants import WRONG_DATA_TYPES
from common.helpers import pop_unused_fields
from common.helpers import run
from schemas.response import FailureResponse
from schemas.response import SelectResponseFailure
from schemas.response import SelectResponseSuccess


@allure.epic("Получение юзера")
@allure.feature("Успешное получение юзера")
@allure.story("Успешное получение юзера по номеру телефона")
def test_success_select_single_user_by_phone(create_user, create_select_by_phone_request, client):
    create_select_by_phone_request["phone"] = create_user["phone"]

    response = run(client.send_message_success(create_select_by_phone_request))

    SelectResponseSuccess(**response)
    check_users(response, len([create_user]), create_user["phone"])


@allure.epic("Получение юзера")
@allure.feature("Успешное получение юзера")
@allure.story("Успешное получение юзера по имени")
def test_success_select_single_user_by_name(create_user, create_select_by_name_request, client):
    create_select_by_name_request["name"] = create_user["name"]

    response = run(client.send_message_success(create_select_by_name_request))

    SelectResponseSuccess(**response)
    check_users(response, len([create_user]), create_user["name"])


@allure.epic("Получение юзера")
@allure.feature("Успешное получение юзера")
@allure.story("Успешное получение юзера по фамилии")
def test_success_select_single_user_by_surname(create_user, create_select_by_surname_request, client):
    create_select_by_surname_request["surname"] = create_user["surname"]

    response = run(client.send_message_success(create_select_by_surname_request))

    SelectResponseSuccess(**response)
    check_users(response, len([create_user]), create_user["surname"])


@allure.epic("Получение юзера")
@allure.feature("Успешное получение юзеров")
@allure.story("Успешное получение нескольких юзеров по имени")
def test_success_select_multiple_users_by_name(create_multiple_users, create_select_by_name_request, client):
    create_select_by_name_request["name"] = create_multiple_users[0]["name"]

    response = run(client.send_message_success(create_select_by_name_request))

    SelectResponseSuccess(**response)
    check_users(response, len([create_multiple_users]), create_multiple_users["surname"])


@allure.epic("Получение юзера")
@allure.feature("Успешное получение юзеров")
@allure.story("Успешное получение нескольких юзеров по фамилии")
def test_success_select_multiple_users_by_surname(create_multiple_users, create_select_by_surname_request, client):
    create_select_by_surname_request["surname"] = create_multiple_users[0]["surname"]

    response = run(client.send_message_success(create_select_by_surname_request))

    SelectResponseSuccess(**response)
    check_users(response, len([create_multiple_users]), create_multiple_users["surname"])


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("Получение юзера по несуществующему номеру телефона")
def test_failure_select_user_not_found(create_select_by_phone_request, client):
    create_select_by_phone_request["phone"] = "123"

    response = run(client.send_message_failure(create_select_by_phone_request))

    SelectResponseFailure(**response)


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("В запросе указаны все поля поиска")
def test_failure_select_all_query_words(create_select_request, client):
    response = run(client.send_message_failure(create_select_request))

    SelectResponseFailure(**response)


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("В запросе отсутствуют поля для поиска")
def test_failure_select_user_no_search(create_select_request, client):
    create_select_request.pop("phone")
    create_select_request.pop("name")
    create_select_request.pop("surname")
    response = run(client.send_message_failure(create_select_request))

    FailureResponse(**response)


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("В запросе отсутствуют обязательные поля")
@pytest.mark.parametrize("param", ["id", "method"])
def test_failure_select_user_no_required_field(create_select_request, client, param):
    create_select_request.pop(param)
    response = run(client.send_message_failure(create_select_request))

    FailureResponse(**response)
    check_failure_reason_no_required_field(response, param)


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("В запросе используется некорректный тип данных")
@pytest.mark.parametrize("param", [*WRONG_DATA_TYPES])
def test_failure_select_user_wrong_structure(client, param):
    response = run(client.send_message_failure(data=param))

    FailureResponse(**response)
    check_failure_reason_wrong_data_type(response)


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("В полях запроса используется некорректный тип данных")
@pytest.mark.parametrize("param", [*SELECT_REQUIRED_PARAMS])
@pytest.mark.parametrize("wrong_type", [*STRING_INCORRECT_DATA_TYPES])
def test_failure_select_user_wrong_fields_type(client, create_select_request, param, wrong_type):
    create_select_request[param] = wrong_type
    data = pop_unused_fields(create_select_request, param)
    response = run(client.send_message_failure(data))

    FailureResponse(**response)
    check_failure_reason_wrong_param_data_type(response)


@allure.epic("Получение юзера")
@allure.feature("Неуспешное получение юзера")
@allure.story("Неудачная попытка SQL инъекции")
def test_failure_select_injection(create_user, create_select_by_name_request, client):
    pattern = "1' or '1' = '1"
    create_select_by_name_request["name"] = pattern
    response = run(client.send_message_failure(create_select_by_name_request))

    SelectResponseFailure(**response)
    assert len(response['users']) == 0
