"""Tests for the `requests` HTTP client."""
import responses
import requests
import pytest

from csobclient.v19.http import RequestsHTTPClient, HTTPTimeoutError


@responses.activate
def test_success_post_json():
    """Test successful post_json."""
    responses.add(responses.POST, "https://example.com", json={"k": "v"})
    response = RequestsHTTPClient().post_json("https://example.com", {})
    assert response.http_success
    assert response.data == {"k": "v"}


@responses.activate
def test_unsuccessful_post_json():
    """Test unsuccessful post_json."""
    responses.add(
        responses.POST, "https://example.com", json={"k": "v"}, status=400
    )
    response = RequestsHTTPClient().post_json("https://example.com", {})
    assert response.http_success is False
    assert response.data == {"k": "v"}


@responses.activate
def test_post_json_timeout():
    """Test post_json timeout."""
    responses.add(
        responses.POST,
        "https://example.com",
        body=requests.Timeout(),
        status=400,
    )

    with pytest.raises(HTTPTimeoutError):
        RequestsHTTPClient().post_json("https://example.com", {})


@responses.activate
def test_get_ok():
    """Test successful get."""
    responses.add(responses.GET, "https://example.com", json={"k": "v"})
    response = RequestsHTTPClient().get("https://example.com")
    assert response.http_success
    assert response.data == {"k": "v"}
