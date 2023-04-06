"""Tests for the `refund_payment` method."""
# pylint:disable=duplicate-code
from csobclient.v19 import Client, PaymentStatus, HTTPResponse
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm

from tests.config import KEY_PATH, KEY
from . import get_fake_http_client


def test_success():
    """Test for the successful payment refund."""

    def _put(*_, **__) -> HTTPResponse:
        return HTTPResponse(
            http_success=True,
            data=mk_payload(
                KEY,
                pairs=(
                    ("payId", "12345"),
                    ("dttm", get_dttm()),
                    ("resultCode", 0),
                    ("resultMessage", "OK"),
                    ("paymentStatus", 10),
                ),
            ),
        )

    client = Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(request=_put),
    )

    info = client.refund_payment("12345")
    assert info.payment_status is PaymentStatus.RETURNED
