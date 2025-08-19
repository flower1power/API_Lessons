from typing import Any

from requests.models import Response

from dm_api_account.models.LoginCredentials import LoginCredentials
from dm_api_account.models.UserEnvelope import UserEnvelope
from rest_client.client import RestClient


class LoginApi(RestClient):
    """
    API клиент для аутентификации пользователей.
    
    Предоставляет методы для входа в систему с использованием
    учетных данных пользователя.
    """

    _v1_login = '/v1/account/login'

    def post_v1_account_login(self, login_data: LoginCredentials, validate_response: bool = True,
                              **kwargs: Any) -> UserEnvelope | Response:
        """
        Аутентификация пользователя по учетным данным.
        
        Args:
            login_data (RequestPostV1Login): Данные для входа в систему
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с результатом аутентификации
        """
        response = self.post(
            path=self._v1_login,
            json=login_data,
            **kwargs
        )

        if validate_response:
            return UserEnvelope(**response.json())

        return response

    def delete_v1_account_login(self, **kwargs: Any) -> Response:
        """
        Выход пользователя из системы на текущем устройстве.
        
        Удаляет текущую сессию пользователя, делая токен аутентификации
        недействительным для текущего устройства.

        Args:
            **kwargs: Дополнительные параметры для HTTP запроса
        
        Returns:
            Response: HTTP ответ от сервера с результатом выхода
            
        Note:
            Требует предварительной авторизации пользователя
            (токен должен быть установлен в заголовках сессии)
        """
        return self.delete(
            path=f'{self._v1_login}',
            **kwargs
        )

    def delete_v1_account_login_all(self, **kwargs: Any) -> Response:
        """
        Выход пользователя из системы на всех устройствах.
        
        Удаляет все активные сессии пользователя, делая все токены
        аутентификации недействительными на всех устройствах.
        
        Args:
            **kwargs: Дополнительные параметры для HTTP запроса

        Returns:
            Response: HTTP ответ от сервера с результатом выхода
            
        Note:
            Требует предварительной авторизации пользователя
            (токен должен быть установлен в заголовках сессии или передан через **kwargs)
        """
        return self.delete(
            path=f'{self._v1_login}/all',
            **kwargs
        )
