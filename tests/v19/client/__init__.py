"""Tests for the client.py."""

import json as jsonlib
from typing import List, Optional

from csobclient.http import HTTPClient, HTTPResponse


def build_http_response(
    code: int = 200,
    body: bytes = b"",
    json: Optional[dict] = None,
    headers: Optional[dict] = None,
) -> HTTPResponse:
    """Build HTTP response."""
    headers = headers or {}
    if json:
        body = jsonlib.dumps(json).encode()
        headers["Content-Type"] = "application/json"

    return HTTPResponse(code, body, headers)


class FakeHTTPClient(HTTPClient):
    # pylint:disable=too-few-public-methods
    """Fake HTTP client."""

    def __init__(self, responses: List[HTTPResponse]) -> None:
        super().__init__()
        self.history = []
        self._responses = responses

    def _request(
        self,
        method: str,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HTTPResponse:
        self.history.append(
            {
                "_method": "request",
                "method": method,
                "url": url,
                "json": json,
                "headers": headers,
            }
        )
        return self._responses.pop(0)
