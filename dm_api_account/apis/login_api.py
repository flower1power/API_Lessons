from typing import TypedDict

import requests


class UserLoginData(TypedDict):
    login: str
    password: str
    rememberMe: bool


class LoginApi:
    def __init__(
            self,
            host: str,
            headers: str = None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account_login(self, json_data: UserLoginData):
        """
         Authenticate via credential
         :param json_data: UserLoginData
         :return: response
         """
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data
        )
        return response
