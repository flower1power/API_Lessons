import allure

@allure.suite("Тесты на проверку метода DELETE v1/account/login")
class TestsDeleteV1AccountLogin:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка выхода пользователя из системы")
    def test_delete_v1_account_login(self, account_helper, prepare_user):
        account_helper.register_new_user(login=prepare_user.login, password=prepare_user.password, email=prepare_user.email)
        account_helper.auth_user(login=prepare_user.login, password=prepare_user.password)
        account_helper.logout_user()