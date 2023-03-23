import allure
from common.errors import DATA_TYPE_EXCEPTION
from common.errors import KEY_NOT_FOUND
from common.errors import KEY_NOT_FOUND_EXCEPTION
from common.errors import PARAM_TYPE_EXCEPTION


@allure.step("Проверяем релевантность выборки юзеров")
def check_selected_users(query: str, users: list):
    for user in users:
        assert query in user.values()


@allure.step("Проверяем юзеров в выборке")
def check_users(response, expected_len, query):
    users = response["users"]
    assert expected_len == len(users)
    check_selected_users(query, users)


@allure.step("Проверяем, что сообщение об ошибке имеет корректный вид")
def check_failure_reason_no_required_field(response, field):
    pattern = f"{KEY_NOT_FOUND_EXCEPTION} {KEY_NOT_FOUND % field}"
    assert pattern in response["reason"]


@allure.step("Проверяем, что сообщение об ошибке имеет корректный вид")
def check_failure_reason_wrong_param_data_type(response):
    pattern = f"{PARAM_TYPE_EXCEPTION}"
    assert pattern in response["reason"]


@allure.step("Проверяем, что сообщение об ошибке имеет корректный вид")
def check_failure_reason_wrong_data_type(response):
    pattern = f"{DATA_TYPE_EXCEPTION}"
    assert pattern in response["reason"]
