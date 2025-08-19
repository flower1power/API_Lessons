from typing import Any

from requests.models import Response

from dm_api_account.models.ChangeEmail import ChangeEmail
from dm_api_account.models.ChangePassword import ChangePassword
from dm_api_account.models.Registration import Registration
from dm_api_account.models.ResetPassword import ResetPassword
from dm_api_account.models.UserDetailsEnvelope import UserDetailsEnvelope
from dm_api_account.models.UserEnvelope import UserEnvelope
from rest_client.client import RestClient


class AccountApi(RestClient):
    """
    API клиент для работы с аккаунтами пользователей.
    
    Предоставляет методы для регистрации, активации, изменения email
    и получения информации о пользователе.
    """

    _v1_account = '/v1/account'

    def post_v1_account(self, reg_data: Registration, **kwargs: Any) -> Response:
        """
        Регистрация нового пользователя.
        
        Args:
            :param reg_data: : Данные для регистрации пользователя
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера с результатом регистрации

        """
        response = self.post(
            path=self._v1_account,
            json=reg_data.model_dump(exclude_none=True),
            **kwargs
        )

        return response

    def get_v1_account(self, validate_response: bool = True, **kwargs: Any) -> Response | UserDetailsEnvelope:
        """
        Получение информации о текущем пользователе.

        Args:
            validate_response (bool): Включение валлидации pydantic
            **kwargs: Дополнительные параметры для HTTP запроса

        Returns:
            Response| UserDetailsEnvelope: HTTP ответ от сервера с информацией о пользователе | UserDetailsEnvelope
        """
        response = self.get(
            path=self._v1_account,
            **kwargs
        )

        if validate_response:
            return UserDetailsEnvelope(**response.json())

        return response

    def put_v1_account_token(
            self,
            token: str,
            validate_response: bool = True,
            **kwargs: Any
    ) -> UserEnvelope | Response:
        """
        Активация зарегистрированного пользователя по токену.
        
        Args:
            token (str): Токен активации, полученный при регистрации
            validate_response (bool): Включение валлидации pydantic
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response | UserEnvelope: HTTP ответ от сервера с результатом активации | UserEnvelope

        """
        headers = {
            'accept': 'text/plain'
        }
        response = self.put(
            path=f'{self._v1_account}/{token}',
            headers=headers,
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    def post_v1_account_password(self, login_data: ResetPassword, validate_response: bool = True,
                                 **kwargs: Any) -> UserEnvelope | Response:
        response = self.post(
            path=f'{self._v1_account}/password',
            json=login_data,
            **kwargs
        )

        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_change_password(self, change_password_data: ChangePassword, validate_response: bool = True,
                                       **kwargs: Any) -> UserEnvelope | Response:
        response = self.put(
            path=f'{self._v1_account}/password',
            headers=self.session.headers,
            json=change_password_data,
            **kwargs
        )

        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_change_email(
            self,
            change_email_data: ChangeEmail,
            validate_response: bool = True,
            **kwargs: Any
    ) -> UserEnvelope | Response:
        """
        Изменение email адреса зарегистрированного пользователя.
        
        Args:
            change_email_data (ChangeEmail): Новые данные пользователя с обновленным email
            validate_response (bool): Включение валлидации pydantic
            **kwargs: Дополнительные параметры для HTTP запроса
            
        Returns:
            Response | UserEnvelope: HTTP ответ от сервера с результатом изменения email | UserEnvelope

        """
        response = self.put(
            path=f'{self._v1_account}/email',
            json=change_email_data,
            **kwargs
        )

        if validate_response:
            return UserEnvelope(**response.json())
        return response
