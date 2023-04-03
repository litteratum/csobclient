"""Tests for the payment module."""
import pytest
from csobclient.v19 import PaymentInfo


@pytest.mark.parametrize(
    ["info", "successful"],
    [
        (PaymentInfo("id", 0, "OK"), True),
        (PaymentInfo("id", 100, "Fail"), False),
    ],
)
def test_ok(info: PaymentInfo, successful: bool):
    """Test for the `ok` field."""
    assert info.ok is successful
