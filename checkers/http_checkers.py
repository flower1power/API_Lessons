from contextlib import contextmanager

import allure
import requests
from requests.exceptions import HTTPError


@allure.step("Проверка ответа http")
@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = ''
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(
                f"Ожидаемый статаус код {expected_status_code} не соврадает с полученным")
        if expected_message:
            raise AssertionError(
                f"Ожидаемое сообщение {expected_message} не соврадает с полученным")
    except HTTPError as error:
        assert error.response.status_code == expected_status_code
        assert error.response.json()['title'] == expected_message
