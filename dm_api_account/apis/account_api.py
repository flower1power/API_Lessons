from typing import TypedDict

import requests


class UserCredentials(TypedDict):
    login: str
    email: str
    password: str


class AccountApi:
    def __init__(self, host: str, headers: str = None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data: UserCredentials):
        """
        Register new user
        :param json_data: UserCredentials
        :return: response
        """
        return requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )

    def put_v1_account_token(self, token: str):
        """
         Activate register user
         :param token: str
         :return: response
         """
        headers = {
            'accept': 'text/plain'
        }
        return requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=headers
        )

    def put_v1_account_change_email(self, json_data: UserCredentials):
        """
        Change registered user email
        :param json_data: UserCredentials
        :return:
        """
        return requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )
