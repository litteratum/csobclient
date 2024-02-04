"""Base client."""

import json as jsonlib
from abc import ABC, abstractmethod
from typing import Optional

_DEFAULT_REQUEST_TIMEOUT = 5


class HTTPRequestError(Exception):
    """Base HTTP request error."""


class HTTPConnectionError(HTTPRequestError):
    """Any error related to connection."""


class HTTPTimeoutError(HTTPRequestError):
    """HTTP request timed out."""


class HTTPInvalidResponseError(HTTPRequestError):
    """HTTP response is invalid."""


class HTTPResponse:
    """HTTP response wrapper."""

    # pylint: disable=too-few-public-methods
    def __init__(
        self, status_code: int, body: Optional[bytes], headers: dict
    ) -> None:
        self.status_code = status_code
        self.body = body or b""
        self._headers = headers

        self._json = None

    @property
    def json(self) -> Optional[dict]:
        """Return body as JSON."""
        if self._json is not None:
            return self._json

        headers = {key.lower(): val for key, val in self._headers.items()}
        if "application/json" in headers.get("content-type", ""):
            try:
                self._json = jsonlib.loads(self.body)
            except Exception as exc:
                raise HTTPInvalidResponseError(
                    f"Invalid JSON in response: {exc}"
                ) from exc

        return self._json

    @property
    def success(self) -> bool:
        """Return whether HTTP request was successful."""
        return self.status_code < 400

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(status={self.status_code})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"status={self.status_code}, "
            f"body={self.body}, "
            f"headers={self._headers}"
            ")"
        )


class HTTPClient(ABC):
    # pylint:disable=too-few-public-methods
    """Base HTTP client."""

    def __init__(self, timeout: int = _DEFAULT_REQUEST_TIMEOUT) -> None:
        self.timeout = timeout

    # pylint: disable=too-many-arguments
    @abstractmethod
    def _request(
        self,
        method: str,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HTTPResponse:
        """Perform request.

        This method must handle all possible HTTP exceptions and raise them
        as `HTTPRequestError`.

        Always use `headers`. You may extend it when needed.

        :param url: API method URL
        :param method: HTTP method
        :param json: JSON data to post
        :param headers: headers to be sent
        """

    def request(
        self,
        method: str,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HTTPResponse:
        """Perform HTTP request with a given HTTP method.

        :param method: HTTP method to use
        :param url: API URL
        :param json: JSON data to post
        :param headers: headers
        """
        return self._request(method, url, json, headers=headers)