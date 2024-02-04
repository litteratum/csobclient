"""Tests for the `refund_payment` method."""

from csobclient.v19 import Client, PaymentStatus
from csobclient.v19.dttm import get_dttm
from csobclient.v19.signature import mk_payload
from tests.config import KEY, KEY_PATH

from . import FakeHTTPClient, build_http_response


def test_success():
    """Test for the successful payment refund."""
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
                            ("paymentStatus", 10),
                        ),
                    )
                )
            ]
        ),
    )

    info = client.refund_payment("12345")
    assert info.payment_status is PaymentStatus.RETURNED
