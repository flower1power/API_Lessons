from typing import TypedDict, Any

from requests.models import Response

from rest_client.client import RestClient


class UserLoginData(TypedDict):
    """
    Структура данных для аутентификации пользователя.
    
    Attributes:
        login (str): Логин пользователя
        password (str): Пароль пользователя
        rememberMe (bool): Флаг "запомнить меня" для сохранения сессии
    """
    login: str
    password: str
    rememberMe: bool


class LoginApi(RestClient):
    """
    API клиент для аутентификации пользователей.
    
    Предоставляет методы для входа в систему с использованием
    учетных данных пользователя.
    """

    _v1_login = '/v1/account/login'

    def post_v1_account_login(self, json_data: UserLoginData, **kwargs: Any) -> Response:
        """
        Аутентификация пользователя по учетным данным.
        
        Args:
            json_data (UserLoginData): Данные для входа в систему
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с результатом аутентификации
        """
        response = self.post(
            path=self._v1_login,
            json=json_data,
            **kwargs
        )
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
