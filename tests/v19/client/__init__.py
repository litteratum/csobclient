"""Tests for the client.py."""
from typing import Callable, Optional

from csobclient.v19.http import HTTPClient, HTTPResponse


def get_fake_http_client(
    get: Optional[Callable] = None, post_json: Optional[Callable] = None
):
    """Return fake HTTP client."""
    if get is None:
        get = lambda url: HTTPResponse(True, {})
    if post_json is None:
        post_json = lambda url, data: HTTPResponse(True, {})

    class _FakeHTTPClient(HTTPClient):
        def post_json(self, url: str, data: dict) -> HTTPResponse:
            return post_json(url, data)

        def get(self, url: str) -> HTTPResponse:
            return get(url)

    return _FakeHTTPClient()
