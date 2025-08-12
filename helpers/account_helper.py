import time
from json import loads

from retrying import retry

from dm_api_account.apis.account_api import UserCredentials
from dm_api_account.apis.login_api import UserLoginData
from services.api_dm_account import ApiDmAccount
from services.api_mailhog import ApiMailhog


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0

        while token is None:
            print(f"Попытка получения токена номер: {count}")
            token = function(*args, **kwargs)
            count += 1

            if token:
                return token

            if count == 5:
                raise AssertionError("Превышено количество попыток получения токена")
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(self, api_dm_account: ApiDmAccount, api_mailhog: ApiMailhog):
        self._dm_account = api_dm_account
        self._mailhog = api_mailhog

    def register_new_user(self, login: str, password: str, email: str):
        json_data: UserCredentials = {
            "login": login,
            "email": email,
            "password": password,
        }

        response = self._dm_account.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login}, не был получен'

        response = self._dm_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь не был активирован'

        return response

    def user_login(self, login: str, password: str, rememberMe: bool = True):
        json_data: UserLoginData = {
            'login': login,
            'password': password,
            'rememberMe': rememberMe
        }

        response = self._dm_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, 'Пользователь не смог авторизоваться'

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login: str):
        token = None
        response = self._mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]

        return token
