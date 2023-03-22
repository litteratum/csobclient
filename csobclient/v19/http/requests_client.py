"""HTTP client which uses `requests` under the hood."""
import requests

from .client import (
    HTTPClient,
    HTTPConnectionError,
    HTTPRequestError,
    HTTPTimeoutError,
    HTTPResponse,
)

_DEFAULT_TIMEOUT = 10


class RequestsHTTPClient(HTTPClient):
    """`requests` HTTP client."""

    def __init__(self) -> None:
        self._session = requests.Session()

    def post_json(self, url: str, data: dict) -> HTTPResponse:
        try:
            response = self._session.post(
                url, json=data, timeout=_DEFAULT_TIMEOUT
            )
            return HTTPResponse(response.ok, response.json())
        except ConnectionError as exc:
            raise HTTPConnectionError(exc) from exc
        except requests.Timeout as exc:
            raise HTTPTimeoutError(exc) from exc
        except requests.RequestException as exc:
            raise HTTPRequestError(exc) from exc

    def get(self, url: str) -> HTTPResponse:
        try:
            response = self._session.get(url, timeout=_DEFAULT_TIMEOUT)
            return HTTPResponse(response.ok, response.json())
        except ConnectionError as exc:
            raise HTTPConnectionError(exc) from exc
        except requests.Timeout as exc:
            raise HTTPTimeoutError(exc) from exc
        except requests.RequestException as exc:
            raise HTTPRequestError(exc) from exc
