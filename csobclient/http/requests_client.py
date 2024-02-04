"""HTTP client which uses `requests` under the hood."""

from typing import Optional

import requests

from .base import (
    _DEFAULT_REQUEST_TIMEOUT,
    HTTPClient,
    HTTPConnectionError,
    HTTPRequestError,
    HTTPResponse,
    HTTPTimeoutError,
)


class RequestsHTTPClient(HTTPClient):
    # pylint: disable=too-few-public-methods
    """`requests` HTTP client."""

    def __init__(self, timeout: int = _DEFAULT_REQUEST_TIMEOUT) -> None:
        super().__init__(timeout)
        self._session = requests.Session()

    # pylint: disable=too-many-arguments
    def _request(
        self,
        method: str,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HTTPResponse:
        try:
            response: requests.Response = getattr(
                self._session, method.lower()
            )(
                url,
                json=json,
                timeout=self.timeout,
                headers=headers,
            )
        except ConnectionError as exc:
            raise HTTPConnectionError(exc) from exc
        except requests.Timeout as exc:
            raise HTTPTimeoutError(exc) from exc
        except requests.RequestException as exc:
            raise HTTPRequestError(exc) from exc

        return HTTPResponse(
            response.status_code, response.content, dict(response.headers)
        )

    def __str__(self) -> str:
        return self.__class__.__name__
