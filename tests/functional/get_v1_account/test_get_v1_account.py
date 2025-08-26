import allure
from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http

@allure.suite("Тесты на проверку метода GET v1/account")
class TestsGetV1Account:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка получения информации об авторизованном пользователе")
    def test_get_v1_account_auth(self, auth_account_helper):
        with check_status_code_http():
            response = auth_account_helper.dm_account.account_api.get_v1_account()

            GetV1Account.check_response_values(response=response, login="DarrenDalton12_08_2025_22_43_04")

    @allure.sub_suite("Негативные тесты")
    @allure.title("Проверка получения информации о неавторизованном пользователе")
    def test_get_v1_account(self, account_helper):
        with check_status_code_http(expected_status_code=401, expected_message='User must be authenticated'):
            account_helper.dm_account.account_api.get_v1_account()