import asyncio
import json
import os

import pytest
import websockets
from websockets.exceptions import ConnectionClosedError

import allure
from settings import HOST
from settings import PORT


@allure.step("Валидируем ответ")
def _validate(data, response, status):
    try:
        resp = json.loads(response)
        assert resp.get("status") == status
        if data and type(data) == dict:
            assert data.get("id") == resp.get("id")
        return resp
    except json.JSONDecodeError:
        print("Failed to decode answer, json expected")
        return response


class Client:
    def __init__(self):
        self.socket = f"ws://{HOST}:{PORT}"

    @allure.step("Отправляем запрос, ожидаем успех")
    async def send_message_success(self, data):
        resp = await self.send(data, "success")
        return resp

    @allure.step("Отправляем запрос, ожидаем ошибку")
    async def send_message_failure(self, data):
        resp = await self.send(data, "failure")
        return resp

    async def send(self, data, status):
        async with websockets.connect(self.socket) as ws:
            try:
                await ws.send(json.dumps(data))
                repl = await ws.recv()
                return _validate(data, repl, status)
            except ConnectionClosedError:
                restart_app()
                pytest.fail(reason="App terminated successfully")
            except ConnectionRefusedError:
                pytest.fail(reason="Connection refused, is App running?")


def run(func):
    return asyncio.get_event_loop().run_until_complete(func)


@allure.step('Рестартим приложение после падения')
def restart_app():
    os.system('make app')


def pop_unused_fields(req_body, param):
    if param == "phone":
        req_body.pop("name")
        req_body.pop("surname")
        return req_body
    if param == "name":
        req_body.pop("phone")
        req_body.pop("surname")
        return req_body
    if param == "surname":
        req_body.pop("name")
        req_body.pop("phone")
        return req_body
