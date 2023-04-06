"""Tests for the `init_payment` method."""
import pytest

from csobclient.v19 import Client, APIError
from csobclient.v19 import HTTPResponse
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm

from tests.config import KEY_PATH, KEY
from . import get_fake_http_client


def test_success():
    """Test for the successful payment init."""

    def _get(url: str, *_, **__) -> HTTPResponse:
        assert "my_ID" in url
        return HTTPResponse(
            http_success=True,
            data=mk_payload(
                KEY,
                pairs=(
                    ("payId", "12345"),
                    ("dttm", get_dttm()),
                    ("resultCode", 0),
                    ("resultMessage", "OK"),
                    ("paymentStatus", 8),
                    ("authCode", "442245"),
                ),
            ),
        )

    client = Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(request=_get),
    )
    client.get_payment_status("my_ID")


def test_api_error():
    """Test for the successful payment init."""

    def _get(*_, **__) -> HTTPResponse:
        return HTTPResponse(
            http_success=False,
            data={
                "resultCode": 140,
                "resultMessage": "Payment not found",
            },
        )

    client = Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(request=_get),
    )

    with pytest.raises(APIError):
        response = client.get_payment_status("my_ID")
        response.raise_for_result_code()
