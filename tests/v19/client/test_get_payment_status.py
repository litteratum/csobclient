"""Tests for the `init_payment` method."""
import pytest

import csobclient
from csobclient.v19.http import HTTPResponse
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm

from tests.config import KEY_PATH
from . import get_fake_http_client


def test_success():
    """Test for the successful payment init."""

    def get(url: str) -> HTTPResponse:
        assert "my_ID" in url
        return HTTPResponse(
            http_success=True,
            data=mk_payload(
                KEY_PATH,
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

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(get=get),
    )
    client.get_payment_status("my_ID")


def test_api_error():
    """Test for the successful payment init."""

    def _get(url: str) -> HTTPResponse:
        return HTTPResponse(
            http_success=False,
            data={
                "resultCode": 140,
                "resultMessage": "Payment not found",
            },
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(get=_get),
    )

    with pytest.raises(csobclient.v19.client.APIError):
        client.get_payment_status("my_ID")
