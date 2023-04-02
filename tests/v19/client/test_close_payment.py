"""Tests for the `close_payment` method."""
# pylint:disable=duplicate-code
import csobclient
from csobclient.v19.http import HTTPResponse
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm
from csobclient.v19 import PaymentStatus

from tests.config import KEY_PATH
from . import get_fake_http_client


def test_success():
    """Test for the successful payment close."""

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
                    ("paymentStatus", 7),
                ),
            ),
        )

    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(request=_put),
    )

    info = client.close_payment("12345")
    assert info.payment_status is PaymentStatus.WAITING_SETTLEMENT
