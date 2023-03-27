"""Tests for the `process_gateway_return` method."""
import csobclient
from csobclient.v19.signature import mk_payload
from csobclient.v19.dttm import get_dttm

from tests.config import KEY_PATH
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
            KEY_PATH,
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
    assert info.payment_status == 7
