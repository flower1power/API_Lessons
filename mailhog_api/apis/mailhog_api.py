from rest_client.client import RestClient


class MailhogApi(RestClient):
    _v2_messages = '/api/v2/messages'

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
        response = self.get(
            path=self._v2_messages,
            params=params,
            verify=False,
            **kwargs
        )
        return response
