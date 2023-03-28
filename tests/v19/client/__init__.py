"""Tests for the client.py."""
from typing import Callable, Optional

from csobclient.v19.http import HTTPClient, HTTPResponse


def get_fake_http_client(request: Optional[Callable] = None):
    """Return fake HTTP client."""
    if request is None:
        request = lambda *_, **__: HTTPResponse(True, {})

    class _FakeHTTPClient(HTTPClient):
        def request(
            self, url: str, method: str = "post", json: Optional[dict] = None
        ) -> HTTPResponse:
            return request(url, method, json)

    return _FakeHTTPClient()
