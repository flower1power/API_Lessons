from typing import Any

from requests.models import Response

from rest_client.client import RestClient


class MailhogApi(RestClient):
    """
    API клиент для работы с Mailhog - почтовым сервисом для тестирования.
    
    Предоставляет методы для получения писем из почтового ящика,
    что полезно для тестирования функциональности регистрации
    и получения токенов активации.
    """

    _v2_messages = '/api/v2/messages'

    def get_api_v2_messages(self, limit: int = 50, **kwargs: Any) -> Response:
        """
        Получение писем из почтового ящика Mailhog.
        
        Args:
            limit (int, optional): Максимальное количество писем для получения. 
            По умолчанию 50
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с письмами
            
        Note:
            Параметр verify=False отключает проверку SSL сертификата
            для локального тестирования.
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
