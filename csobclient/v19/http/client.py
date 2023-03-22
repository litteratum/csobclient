"""HTTP base client."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


class HTTPRequestError(Exception):
    """Base HTTP request error."""


class HTTPConnectionError(HTTPRequestError):
    """Any error related to connection."""


class HTTPTimeoutError(HTTPRequestError):
    """HTTP request timed out."""


@dataclass
class HTTPResponse:
    """HTTP response wrapper."""

    http_success: bool
    data: dict


class HTTPClient(ABC):
    """Base HTTP client."""

    @abstractmethod
    def post_json(self, url: str, data: dict) -> HTTPResponse:
        """Post JSON.

        This method must POST data with application/json content type
        and return API response. API response is expected to be JSON.

        :param url: API method URL
        :param data: JSON data to post

        :raises HTTPConnectionError: if connection fails
        :raises HTTPTimeoutError: if request timeouts
        :raises HTTPRequestError: for any other exception
        """

    @abstractmethod
    def get(self, url: str) -> HTTPResponse:
        """GET request.

        This method must send GET request to the `url` and return JSON
        response.

        :param url: API method URL

        :raises HTTPConnectionError: if connection fails
        :raises HTTPTimeoutError: if request timeouts
        :raises HTTPRequestError: for any other exception
        """
