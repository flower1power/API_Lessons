import allure

@allure.suite("Тесты на проверку метода PUT v1/account/token")
class TestsPutV1AccountToken:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка активации пользователя по токену")
    def test_put_v1_account_token(self, account_helper, prepare_user):
        account_helper.register_new_user(login=prepare_user.login, password=prepare_user.password, email=prepare_user.email)