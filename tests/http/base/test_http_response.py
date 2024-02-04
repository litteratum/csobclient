"""Tests for the HTTP response."""

from csobclient.http.base import HTTPResponse


def test_json_returns_none_if_content_type_is_not_json():
    """Test the `json` property.

    It must return None if content-type does not contain "application/json".
    """
    assert (
        HTTPResponse(
            200, b'{"any": "json"}', {"ConTent-Type": "text/plain"}
        ).json
        is None
    )


def test_json_returns_json_if_content_type_is_json():
    """Test the `json` property.

    It must return JSON loaded form body if content-type contains
    "application/json".
    """
    assert HTTPResponse(
        200, b'{"any": "json"}', {"ConTent-Type": "application/json;utf8"}
    ).json == {"any": "json"}


def test_json_is_cached():
    """Test the `json` property.

    It must cache loaded JSON and always return it.
    """
    resp = HTTPResponse(
        200, b'{"any": "json"}', {"ConTent-Type": "application/json;utf8"}
    )
    assert resp.json == {"any": "json"}
    resp.body = b'{"new": "json"}'
    assert resp.json == {"any": "json"}
