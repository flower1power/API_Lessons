from typing import TypedDict

from rest_client.client import RestClient


class UserCredentials(TypedDict):
    login: str
    email: str
    password: str


class AccountApi(RestClient):
    _v1_account = '/v1/account'

    def post_v1_account(self, json_data: UserCredentials, **kwargs):
        """
        Register new user
        :param json_data: UserCredentials
        :param **kwargs: дополнительные аргументы для requests.post
        :return: response
        """
        return self.post(
            path=self._v1_account,
            json=json_data,
            **kwargs
        )

    def put_v1_account_token(self, token: str, **kwargs):
        """
        Activate register user
        :param token: str
        :param **kwargs: дополнительные аргументы для requests.put
        :return: response
        """
        headers = {
            'accept': 'text/plain'
        }
        return self.put(
            path=f'{self._v1_account}/{token}',
            headers=headers,
            **kwargs
        )

    def put_v1_account_change_email(self, json_data: UserCredentials, **kwargs):
        """
        Change registered user email
        :param json_data: UserCredentials
        :param **kwargs: дополнительные аргументы для requests.put
        :return:
        """
        return self.put(
            path=f'{self._v1_account}/email',
            json=json_data,
            **kwargs
        )
