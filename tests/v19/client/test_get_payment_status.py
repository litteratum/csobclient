"""Tests for the `init_payment` method."""

import pytest

from csobclient.v19 import APIError, Client
from csobclient.v19.dttm import get_dttm
from csobclient.v19.signature import mk_payload
from tests.config import KEY, KEY_PATH

from . import FakeHTTPClient, build_http_response


def test_success():
    """Test for the successful payment init."""
    client = Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=FakeHTTPClient(
            responses=[
                build_http_response(
                    json=mk_payload(
                        KEY,
                        pairs=(
                            ("payId", "12345"),
                            ("dttm", get_dttm()),
                            ("resultCode", 0),
                            ("resultMessage", "OK"),
                            ("paymentStatus", 8),
                            ("authCode", "442245"),
                        ),
                    )
                )
            ]
        ),
    )
    client.get_payment_status("my_ID")


def test_api_error():
    """Test for the successful payment init."""
    client = Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=FakeHTTPClient(
            responses=[
                build_http_response(
                    code=400,
                    json={
                        "resultCode": 140,
                        "resultMessage": "Payment not found",
                    },
                )
            ]
        ),
    )

    with pytest.raises(APIError):
        response = client.get_payment_status("my_ID")
        response.raise_for_result_code()
