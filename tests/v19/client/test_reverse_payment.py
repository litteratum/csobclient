"""Tests for the `reverse_payment` method."""

import pytest

from csobclient.v19 import APIError, Client, PaymentStatus
from csobclient.v19.dttm import get_dttm
from csobclient.v19.signature import mk_payload
from tests.config import KEY, KEY_PATH

from . import FakeHTTPClient, build_http_response


def test_success():
    """Test for the successful payment reversal."""
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
                            ("paymentStatus", 5),
                        ),
                    )
                )
            ]
        ),
    )

    info = client.reverse_payment("12345")
    assert info.payment_status is PaymentStatus.REVERSED


def test_api_error():
    """Test for the unsuccessful payment reversal."""
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
                            ("resultCode", 150),
                            ("resultMessage", "Payment not in valid state"),
                            ("paymentStatus", 6),
                        ),
                    )
                )
            ]
        ),
    )

    with pytest.raises(APIError) as exc:
        response = client.reverse_payment("12345")
        response.raise_for_result_code()

    assert exc.value.code == 150
