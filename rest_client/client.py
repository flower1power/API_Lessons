import uuid
from typing import Literal, Any, Dict, Optional
from urllib.parse import urljoin

import curlify
import structlog
from requests import session
from requests.exceptions import JSONDecodeError
from requests.models import Response
from swagger_coverage_py.listener import RequestSchemaHandler
from swagger_coverage_py.uri import URI

from rest_client.configuration import Configuration
from rest_client.utilites import allure_attach

HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


class RestClient:
    """
    Базовый HTTP клиент для работы с REST API.
    
    Предоставляет методы для выполнения HTTP запросов (GET, POST, PUT, DELETE)
    с автоматическим логированием, генерацией cURL команд и обработкой ответов.
    Поддерживает настройку заголовков, базового URL и отключение логирования.
    """

    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.session = session()
        self.log = structlog.getLogger(__name__).bind(service='api')

    def set_headers(self, headers: dict[str, str] | None) -> None:
        """
        Установка заголовков для HTTP запросов.
        
        Args:
            headers (Optional[Dict[str, str]]): Словарь заголовков для установки.
            Если None, заголовки не изменяются
        """
        if headers:
            self.session.headers.update(headers)

    def get(self, path: str, **kwargs: Any) -> Response:
        """
        Выполнение GET запроса.
        
        Args:
            path (str): Путь к эндпоинту API
            **kwargs: Дополнительные параметры для HTTP запроса
            (params, headers, timeout и т.д.)
            
        Returns:
            Response: HTTP ответ от сервера
        """
        return self._send_request(method="GET", path=path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        """
        Выполнение POST запроса.
        
        Args:
            path (str): Путь к эндпоинту API
            **kwargs: Дополнительные параметры для HTTP запроса
            (json, data, headers, timeout и т.д.)
            
        Returns:
            Response: HTTP ответ от сервера
        """
        return self._send_request(method="POST", path=path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        """
        Выполнение PUT запроса.
        
        Args:
            path (str): Путь к эндпоинту API
            **kwargs: Дополнительные параметры для HTTP запроса
            (json, data, headers, timeout и т.д.)
            
        Returns:
            Response: HTTP ответ от сервера
        """
        return self._send_request(method="PUT", path=path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        """
        Выполнение DELETE запроса.
        
        Args:
            path (str): Путь к эндпоинту API
            **kwargs: Дополнительные параметры для HTTP запроса
            (headers, timeout и т.д.)
            
        Returns:
            Response: HTTP ответ от сервера
        """
        return self._send_request(method="DELETE", path=path, **kwargs)

    @allure_attach
    def _send_request(self, method: HttpMethod, path: str, **kwargs: Any) -> Response:
        """
        Внутренний метод для выполнения HTTP запросов.
        
        Выполняет запрос, логирует детали запроса и ответа,
        генерирует cURL команду для отладки.
        
        Args:
            method (HttpMethod): HTTP метод (GET, POST, PUT, DELETE)
            path (str): Путь к эндпоинту API
            **kwargs: Параметры для HTTP запроса
            
        Returns:
            Response: HTTP ответ от сервера
        """
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = urljoin(self.host, path.lstrip("/"))

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )

        rest_response = self.session.request(method=method, url=full_url, **kwargs)

        uri = URI(host=self.host, base_path="", unformatted_path=path, uri_params=kwargs.get('params'))

        RequestSchemaHandler(
            uri=uri, method=method.lower(), response=rest_response, kwargs=kwargs
        ).write_schema()

        curl = curlify.to_curl(rest_response.request)
        print(curl)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response=rest_response),
        )

        rest_response.raise_for_status()
        return rest_response

    @staticmethod
    def _get_json(rest_response: Response) -> dict[str, Any]:
        """
        Извлечение JSON данных из HTTP ответа.
        
        Безопасно извлекает JSON из ответа, возвращая пустой словарь
        в случае ошибки декодирования.
        
        Args:
            rest_response (Response): HTTP ответ для извлечения JSON
            
        Returns:
            Dict[str, Any]: JSON данные или пустой словарь при ошибке
        """
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
