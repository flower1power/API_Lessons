import requests


class MailhogApi:
    def __init__(self, host: str, headers: str = None):
        self.host = host
        self.headers = headers

    def get_api_v2_messages(self, limit: int = 50, **kwargs):
        """
        Get user emails
        :param limit: int = 50
        :param **kwargs: дополнительные аргументы для requests.post
        :return: response
        """
        params = {
            'limit': limit,

        }
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params,
            verify=False,
            **kwargs
        )
        return response
