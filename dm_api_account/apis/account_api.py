from typing import TypedDict, Any

from requests.models import Response

from rest_client.client import RestClient


class UserCredentials(TypedDict):
    """
    Структура данных для учетных данных пользователя.
    
    Attributes:
        login (str): Логин пользователя
        email (str): Email адрес пользователя
        password (str): Пароль пользователя
    """
    login: str
    email: str
    password: str


class RequestChangePassword(TypedDict):
    """
    Структура данных для учетных данных пользователя.

    Attributes:
        login (str): Логин пользователя
        token (str): Токен смены пароля
        oldPassword (str): старый пароль пользователя
        newPassword (str): новый пароль пользователя
    """
    login: str
    token: str
    oldPassword: str
    newPassword: str


class AccountApi(RestClient):
    """
    API клиент для работы с аккаунтами пользователей.
    
    Предоставляет методы для регистрации, активации, изменения email
    и получения информации о пользователе.
    """

    _v1_account = '/v1/account'

    def post_v1_account(self, json_data: UserCredentials, **kwargs: Any) -> Response:
        """
        Регистрация нового пользователя.
        
        Args:
            json_data (UserCredentials): Данные для регистрации пользователя
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с результатом регистрации
        """
        return self.post(
            path=self._v1_account,
            json=json_data,
            **kwargs
        )

    def put_v1_account_token(self, token: str, **kwargs: Any) -> Response:
        """
        Активация зарегистрированного пользователя по токену.
        
        Args:
            token (str): Токен активации, полученный при регистрации
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с результатом активации
        """
        headers = {
            'accept': 'text/plain'
        }
        response = self.put(
            path=f'{self._v1_account}/{token}',
            headers=headers,
            **kwargs
        )

        return response

    def put_v1_account_change_email(self, json_data: UserCredentials, **kwargs: Any) -> Response:
        """
        Изменение email адреса зарегистрированного пользователя.
        
        Args:
            json_data (UserCredentials): Новые данные пользователя с обновленным email
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с результатом изменения email
        """
        return self.put(
            path=f'{self._v1_account}/email',
            json=json_data,
            **kwargs
        )

    def get_v1_account(self, **kwargs: Any) -> Response:
        """
        Получение информации о текущем пользователе.
        
        Args:
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с информацией о пользователе
        """
        return self.get(
            path=self._v1_account,
            **kwargs
        )

    def post_v1_account_password(self, login: str, email: str, **kwargs: Any) -> Response:
        return self.post(
            path=f'{self._v1_account}/password',
            json={
                "login": login,
                "email": email
            },
            **kwargs
        )

    def put_v1_account_change_password(self, json_data: RequestChangePassword, **kwargs: Any) -> Response:
        return self.put(
            path=f'{self._v1_account}/password',
            headers=self.session.headers,
            json=json_data,
            **kwargs
        )
