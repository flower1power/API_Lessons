from typing import TypedDict

from rest_client.client import RestClient


class UserLoginData(TypedDict):
    login: str
    password: str
    rememberMe: bool


class LoginApi(RestClient):
    _v1_login = '/v1/account/login'

    def post_v1_account_login(self, json_data: UserLoginData, **kwargs):
        """
        Authenticate via credential
        :param json_data: UserLoginData
        :param **kwargs: дополнительные аргументы для requests.post
        :return: response
        """
        response = self.post(
            path=self._v1_login,
            json=json_data,
            **kwargs
        )
        return response
