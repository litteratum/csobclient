"""Tests for the address module."""
import pytest
from csobclient.v19 import order


@pytest.mark.parametrize(
    ["address", "city", "zip_code", "address2", "address3"],
    [
        ("a" * 51, "city", "zip", "address2", "address3"),
        ("address", "a" * 51, "zip", "address2", "address3"),
        ("address", "city", "a" * 17, "address2", "address3"),
        ("address", "city", "zip", "a" * 51, "address3"),
        ("address", "city", "zip", "address2", "a" * 51),
    ],
)
def test_address_invalid_args(
    address: str, city: str, zip_code: str, address2: str, address3: str
):
    """Test for the invalid CartItem args."""
    with pytest.raises(ValueError):
        order.AddressData(
            address, "CZE", city, zip_code, "state", address2, address3
        )
