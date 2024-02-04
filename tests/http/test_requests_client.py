"""Tests for the `requests` HTTP client."""

import pytest
import requests
import responses

from csobclient.http import HTTPTimeoutError
from csobclient.http.requests_client import RequestsHTTPClient

from . import _build_url


def _build_http_client() -> RequestsHTTPClient:
    return RequestsHTTPClient()


@responses.activate
def test_success_post_json():
    """Test successful post_json."""
    url = _build_url()
    responses.add(responses.POST, url, json={"k": "v"})
    assert {"k": "v"} == _build_http_client().request(
        "post", url, json={}
    ).json


@responses.activate
def test_unsuccessful_post_json():
    """Test unsuccessful post_json."""
    url = _build_url("test")
    data = {"code": "POS_ERROR", "message": "dummyerror"}
    responses.add(
        responses.POST,
        url,
        json=data,
        status=400,
    )

    assert (
        _build_http_client().request("post", url, json={}).status_code == 400
    )


@responses.activate
def test_post_json_timeout():
    """Test post_json timeout."""
    url = _build_url()
    responses.add(
        responses.POST, _build_url(), body=requests.Timeout(), status=400
    )

    with pytest.raises(HTTPTimeoutError):
        _build_http_client().request("post", url, json={})


@responses.activate
def test_get_ok():
    """Test successful get."""
    url = _build_url("order")
    responses.add(responses.GET, url, json={"k": "v"})
    assert {"k": "v"} == _build_http_client().request("get", url).json


@responses.activate
def test_empty_body():
    """Test for empty body processing.

    It is OK if the content-type is not application/json.
    """
    url = _build_url()
    responses.add(responses.POST, url)
    assert _build_http_client().request("post", url, json={}).body == b""
