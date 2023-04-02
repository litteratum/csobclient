"""Tests for the `reverse_payment` method."""
# pylint:disable=duplicate-code
import pytest
import csobclient
from csobclient.v19.client import APIError
from csobclient.v19.http import HTTPResponse
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm
from csobclient.v19 import PaymentStatus

from tests.config import KEY_PATH
from . import get_fake_http_client


def test_success():
    """Test for the successful payment reversal."""

    def _put(*_, **__) -> HTTPResponse:
        return HTTPResponse(
            http_success=True,
            data=mk_payload(
                KEY_PATH,
                pairs=(
                    ("payId", "12345"),
                    ("dttm", get_dttm()),
                    ("resultCode", 0),
                    ("resultMessage", "OK"),
                    ("paymentStatus", 5),
                ),
            ),
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(request=_put),
    )

    info = client.reverse_payment("12345")
    assert info.payment_status is PaymentStatus.REVERSED


def test_api_error():
    """Test for the unsuccessful payment reversal."""

    def _put(*_, **__) -> HTTPResponse:
        return HTTPResponse(
            http_success=True,
            data=mk_payload(
                KEY_PATH,
                pairs=(
                    ("payId", "12345"),
                    ("dttm", get_dttm()),
                    ("resultCode", 150),
                    ("resultMessage", "Payment not in valid state"),
                    ("paymentStatus", 6),
                ),
            ),
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(request=_put),
    )

    with pytest.raises(APIError) as exc:
        client.reverse_payment("12345")

    assert exc.value.code == 150
