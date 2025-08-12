import uuid
from typing import Literal
from urllib.parse import urljoin

import curlify
import structlog
from requests import session
from requests.exceptions import JSONDecodeError

HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]


class RestClient:

    def __init__(self, host: str, headers: str = None):
        self.host = host
        self.headers = headers
        self.session = session()
        self.log = structlog.getLogger(__name__).bind(service='api')

    def get(self, path: str, **kwargs):
        return self._send_request(method="GET", path=path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._send_request(method="POST", path=path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._send_request(method="PUT", path=path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._send_request(method="DELETE", path=path, **kwargs)

    def _send_request(self, method: HttpMethod, path: str, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = urljoin(self.host, path.lstrip("/"))

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

        curl = curlify.to_curl(rest_response.request)
        print(curl)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response=rest_response),
        )

        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
