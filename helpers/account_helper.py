import time
from json import loads, JSONDecodeError
from typing import Any, Callable, NoReturn

import allure
from requests.models import Response

from dm_api_account.models.ChangeEmail import ChangeEmail
from dm_api_account.models.ChangePassword import ChangePassword
from dm_api_account.models.LoginCredentials import LoginCredentials
from dm_api_account.models.Registration import Registration
from dm_api_account.models.ResetPassword import ResetPassword
from dm_api_account.models.UserEnvelope import UserEnvelope
from services.api_dm_account import ApiDmAccount
from services.api_mailhog import ApiMailhog


def retry_if_result_none(result: Any) -> bool:
    """
    Проверяет, является ли результат None для механизма повторных попыток.
    
    Args:
        result (T): Результат функции для проверки
        
    Returns:
        bool: True если результат None, False в противном случае
    """
    return result is None


def retrier(function: Callable[..., str | NoReturn]) -> Callable[..., str | NoReturn]:
    """
    Декоратор для повторного выполнения функции до получения результата.
    
    Выполняет функцию до 5 раз с интервалом в 1 секунду, пока не получит
    не-None результат или не превысит лимит попыток.
    
    Args:
        function (Callable[..., T]): Функция для декорирования
        
    Returns:
        Callable[..., T]: Обернутая функция с логикой повторных попыток
        
    Raises:
        AssertionError: Если превышено количество попыток (5)
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        token = None
        count = 0
        sleep = 1

        while token is None:
            print(f"Попытка получения токена номер: {count}")
            token = function(*args, **kwargs)
            count += 1

            if token:
                return token

            if count == 10:
                raise AssertionError("Превышено количество попыток получения токена")
            sleep = sleep * (count / 3)
            time.sleep(sleep)

    return wrapper


class AccountHelper:
    """
    Вспомогательный класс для работы с аккаунтами пользователей.
    
    Предоставляет высокоуровневые методы для регистрации, авторизации
    и управления пользователями через API.
    """

    def __init__(self, api_dm_account: ApiDmAccount, api_mailhog: ApiMailhog):
        self.dm_account = api_dm_account
        self.mailhog = api_mailhog

    @allure.step("Регистрация нового пользователя с последующей активацией")
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str,
            validate_response=True
    ) -> Response | UserEnvelope:
        """
        Регистрация нового пользователя с последующей активацией.
        
        Создает нового пользователя, получает токен активации из почты
        и активирует аккаунт.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            email (str): Email адрес пользователя
            validate_response (bool): Отключение валлидации pydantic
            
        Returns:
            Response: HTTP ответ от сервера после активации пользователя
            
        Raises:
            AssertionError: Если пользователь не был создан, токен не получен
            или пользователь не был активирован
        """

        reg_data = Registration(
            login=login,
            password=password,
            email=email
        )

        self.dm_account.account_api.post_v1_account(reg_data=reg_data)

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login}, не был получен'

        response = self.dm_account.account_api.put_v1_account_token(
            token=token,
            validate_response=validate_response
        )

        if validate_response:
            return response

        return response

    @allure.step("Авторизация пользователя в системе")
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False,

    ) -> Response | UserEnvelope:
        """
        Авторизация пользователя в системе.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            remember_me (bool, optional): Флаг "запомнить меня". По умолчанию True
            validate_response (bool): Отключение валлидации pydantic
            validate_headers (bool): Отключение валлидации headers
            
        Returns:
            Response: HTTP ответ от сервера с результатом авторизации
            
        Raises:
            AssertionError: Если пользователь не смог авторизоваться
        """

        login_data = LoginCredentials(
            login=login,
            password=password,
            rememberMe=remember_me
        )

        response = self.dm_account.login_api.post_v1_account_login(
            login_data=login_data,
            validate_response=validate_response
        )

        if validate_response:
            return response

        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"

        return response

    @allure.step("Авторизация клиента и установка токена аутентификации в заголовки")
    def auth_user(self, login: str, password: str, remember_me: bool = True, validate_response=False) -> None:
        """
        Авторизация клиента и установка токена аутентификации в заголовки.
        
        Выполняет вход в систему и устанавливает полученный токен
        в заголовки для последующих запросов.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            remember_me (bool, optional): Флаг "запомнить меня". По умолчанию True
            validate_response (bool): Отключение валлидации pydantic

        Raises:
            AssertionError: Если пользователь не смог авторизоваться
        """

        response = self.user_login(
            login=login,
            password=password,
            remember_me=remember_me,
            validate_response=validate_response
        )

        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}

        self.dm_account.account_api.set_headers(token)
        self.dm_account.login_api.set_headers(token)

    @retrier
    @allure.step("Получение токена активации для пользователя по логину")
    def get_activation_token_by_login(self, login: str) -> str:
        """
        Получение токена активации для пользователя по логину.
        
        Ищет письмо с токеном активации в почтовом ящике Mailhog
        для указанного пользователя.
        
        Args:
            login (str): Логин пользователя для поиска токена
            
        Returns:
            str: Токен активации пользователя
            
        Raises:
            AssertionError: Если письма не были получены
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            try:
                user_data = loads(item['Content']['Body'])
            except JSONDecodeError:
                continue
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break

        return token

    @retrier
    @allure.step("Получение токена сброса пароля для пользователя по логину")
    def get_reset_password_token_by_login(self, login: str) -> str:
        """
        Получение токена сброса пароля для пользователя по логину.
        
        Ищет письмо с токеном сброса пароля в почтовом ящике Mailhog
        для указанного пользователя. Токен используется для смены пароля
        через API.
        
        Args:
            login (str): Логин пользователя для поиска токена
            
        Returns:
            str: Токен сброса пароля пользователя
            
        Raises:
            AssertionError: Если письма не были получены
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            try:
                user_data = loads(item['Content']['Body'])
            except JSONDecodeError:
                continue
            user_login = user_data.get('Login')
            if user_login == login:
                if 'ConfirmationLinkUri' in user_data:
                    token = user_data['ConfirmationLinkUri'].split('/')[-1]
                    break

        return token

    @allure.step("Смена пароля пользователя")
    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str,
            validate_response: bool = True
    ) -> Response | UserEnvelope:
        """
        Смена пароля пользователя с использованием токена сброса пароля.
        
        Процесс смены пароля включает:
        1. Запрос на сброс пароля через API
        2. Получение токена сброса пароля из письма
        3. Выполнение запроса на изменение пароля
        
        Args:
            login (str): Логин пользователя
            email (str): Email адрес пользователя
            old_password (str): Текущий пароль пользователя
            new_password (str): Новый пароль пользователя
            validate_response (bool): Включение валлидации pydantic

            
        Returns:
            Response: HTTP ответ от сервера с результатом смены пароля
            
        Raises:
            AssertionError: Если токен сброса пароля не получен или смена пароля не удалась
        """

        login_data = ResetPassword(
            login=login,
            email=email
        )

        self.dm_account.account_api.post_v1_account_password(
            login_data=login_data,
            validate_response=validate_response
        )

        reset_token = self.get_reset_password_token_by_login(login=login)
        assert reset_token is not None, f'Токен для сброса пароля пользователя {login} не был получен'

        change_password_data = ChangePassword(
            login=login,
            token=reset_token,
            oldPassword=old_password,
            newPassword=new_password
        )

        response = self.dm_account.account_api.put_v1_account_change_password(
            change_password_data=change_password_data,
            validate_response=validate_response
        )

        if validate_response:
            return response

        assert response.status_code == 200, 'Не удалось изменить пароль'
        return response

    @allure.step("Смена почты пользователя")
    def change_email(
            self,
            login: str,
            password: str,
            new_email: str,
            validate_response: bool = True
    ) -> Response | UserEnvelope:

        change_email_data = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )

        response = self.dm_account.account_api.put_v1_account_change_email(
            change_email_data=change_email_data,
            validate_response=validate_response
        )

        if validate_response:
            return response

        return response

    @allure.step("Выход пользователя из системы на текущем устройстве")
    def logout_user(self, token: str | None = None, **kwargs: Any) -> Response:
        """
        Выход пользователя из системы на текущем устройстве.

        По умолчанию использует текущие заголовки сессии клиента. Можно передать
        конкретный `token`, чтобы разлогинить определённую сессию, отличную от
        той, что установлена в сессии клиента. 

        Args:
            token (str | None): Опциональный токен `x-dm-auth-token` для разлогина
                конкретной сессии.
            **kwargs: Дополнительные параметры для HTTP запроса

        Returns:
            Response: HTTP ответ от сервера с результатом выхода

        Note:
            Требует предварительной авторизации пользователя или явной
            передачи токена через аргумент `token` или `headers`.
        """

        if token:
            kwargs['headers'] = {**kwargs.get('headers'), 'x-dm-auth-token': token}

        response = self.dm_account.login_api.delete_v1_account_login(**kwargs)

        return response

    @allure.step("Выход пользователя из системы на всех устройствах")
    def logout_user_all_device(self, token: str | None = None, **kwargs: Any) -> Response:
        """
        Выход пользователя из системы на всех устройствах.
        
        Удаляет все активные сессии пользователя, делая все токены
        аутентификации недействительными на всех устройствах.
        По умолчанию использует текущие заголовки сессии клиента. Можно передать
        конкретный `token`. 
        
        Args:
            token (str | None): Опциональный токен `x-dm-auth-token` для разлогина
                конкретной сессии.
            **kwargs: Дополнительные параметры для HTTP запроса

        Returns:
            Response: HTTP ответ от сервера с результатом выхода
            
        Note:
            Требует предварительной авторизации пользователя или явной
            передачи токена через аргумент `token` или `headers`.
        """
        if token:
            kwargs['headers'] = {**kwargs.get('headers'), 'x-dm-auth-token': token}

        response = self.dm_account.login_api.delete_v1_account_login_all()

        return response

    @allure.step("Активация зарегистрированного пользователя по токену")
    def activate_user(self, token: str, validate_response: bool = True, ) -> Response | UserEnvelope:
        """
        Активация зарегистрированного пользователя по токену.

        Args:
            token (str): Токен активации, полученный при регистрации
            validate_response (bool): Включение валлидации pydantic
            **kwargs: Дополнительные параметры для HTTP запроса

        Returns:
            Response: HTTP ответ от сервера с результатом активации
        """

        response = self.dm_account.account_api.put_v1_account_token(token=token, validate_response=validate_response)

        if validate_response:
            return response

        assert response.status_code == 200, 'Не удалось активировать токен'
        return response
