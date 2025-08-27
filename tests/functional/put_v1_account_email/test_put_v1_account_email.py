import allure
from faker import Faker

from checkers.http_checkers import check_status_code_http

@allure.suite("Тесты на проверку метода PUT v1/account/email")
class TestsPutV1AccountEmail:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка смены почты пользователя")
    def test_put_v1_account_email(self, account_helper, prepare_user):
        faker = Faker()
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = f'{prepare_user.login}{faker.text(5)}@mail.ru'
        expected_error_text = 'User is inactive. Address the technical support for more details'

        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        account_helper.change_email(login=login, password=password, new_email=new_email)

        with check_status_code_http(403, expected_error_text):
            account_helper.user_login(login=login, password=password)

        token = account_helper.get_activation_token_by_login(login=login)
        account_helper.activate_user(token=token)
        account_helper.user_login(login=login, password=password)