"""Tests for the `init_payment` method."""
import base64
import pytest

import csobclient
from csobclient.v19.http import HTTPResponse
from csobclient.v19.signature import mk_payload, InvalidSignatureError
from csobclient.v19.dttm import get_dttm
from csobclient.v19.cart import Cart, CartItem

from tests.config import KEY_PATH
from . import get_fake_http_client

_CLIENT = csobclient.Client("id", "url", "pvk", "pk")


@pytest.mark.parametrize(
    ["ttl_sec"],
    [
        (0,),
        (-1,),
        (299,),
        (1801,),
    ],
)
def test_invalid_ttl_sec(ttl_sec: int):
    """Test for the invalid ttl_sec values."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment(
            "order_no", 100, "http://127.0.0.1", ttl_sec=ttl_sec
        )


def test_invalid_order_no():
    """Test for the invalid order_no value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment("1" * 11, 100, "http://127.0.0.1")


def test_invalid_return_url():
    """Test for the invalid return_url value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment("123", 100, "a" * 301)


def test_invalid_customer_id():
    """Test for the invalid customer_id value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment(
            "123", 100, "http://127.0.0.1", customer_id="a" * 51
        )


def test_to_long_merchant_data():
    """Test for the invalid merchant data value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment(
            "123",
            100,
            "http://127.0.0.1",
            customer_id="id",
            merchant_data=b"0" * 300,
        )


def test_success():
    """Test for the successful payment init."""

    def post_json(url: str, data: dict) -> HTTPResponse:
        return HTTPResponse(
            http_success=True,
            data=mk_payload(
                KEY_PATH,
                pairs=(
                    ("payId", "12345"),
                    ("dttm", get_dttm()),
                    ("resultCode", 0),
                    ("resultMessage", "OK"),
                    ("paymentStatus", 1),
                ),
            ),
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(post_json=post_json),
    )
    client.init_payment(
        "oder_no",
        100,
        "http://success.com",
        cart=Cart([CartItem("item1", 2, 10), CartItem("item2", 1, 90)]),
        merchant_data=b"hello",
    )


def test_api_error():
    """Test for the failed payment init.

    API error.
    """

    def post_json(url: str, data: dict) -> HTTPResponse:
        return HTTPResponse(
            http_success=True,
            data={
                "resultCode": 100,
                "resultMessage": "Missing parameter merchantId",
            },
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(post_json=post_json),
    )

    with pytest.raises(csobclient.v19.client.APIError):
        client.init_payment("oder_no", 100, "http://success.com")


@pytest.mark.parametrize(
    "signature",
    [
        "any",
        base64.b64encode(b"any").decode(),
        "",
    ],
)
def test_invalid_signature(signature: str):
    """Test for the invalid response signature."""

    def post_json(url: str, data: dict) -> HTTPResponse:
        return HTTPResponse(
            http_success=True,
            data={"signature": signature, "resultCode": 0},
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(post_json=post_json),
    )

    with pytest.raises(InvalidSignatureError):
        client.init_payment("oder_no", 100, "http://success.com")