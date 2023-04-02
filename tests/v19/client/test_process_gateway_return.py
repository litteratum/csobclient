"""Tests for the `process_gateway_return` method."""
# pylint:disable=duplicate-code
import csobclient
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm
from csobclient.v19 import PaymentStatus

from tests.config import KEY_PATH, KEY
from . import get_fake_http_client


def test_success():
    """Test for the successful gateway return processing."""
    client = csobclient.Client(
        "id",
        KEY_PATH,
        KEY_PATH,
        http_client=get_fake_http_client(),
    )

    info = client.process_gateway_return(
        mk_payload(
            KEY,
            pairs=(
                ("payId", "12345"),
                ("dttm", get_dttm()),
                ("resultCode", "0"),
                ("resultMessage", "OK"),
                ("paymentStatus", "7"),
                ("authCode", "442245"),
                ("merchantData", "SGVsbG8="),
            ),
        ),
    )

    assert info.pay_id == "12345"
    assert info.merchant_data == b"Hello"
    assert info.payment_status is PaymentStatus.WAITING_SETTLEMENT
