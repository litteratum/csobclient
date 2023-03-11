"""Tests for the cart module."""
from typing import Optional
import pytest
from csobclient.v19.cart import Cart, CartItem


def test_cart_item_as_json():
    """Test for the CartItem.as_json()."""
    item = CartItem("example_name", 10, 100)
    assert item.as_json() == {
        "name": "example_name",
        "quantity": 10,
        "amount": 100,
    }

    item.description = "desc"
    assert item.as_json()["description"] == "desc"


@pytest.mark.parametrize(
    ["name", "quantity", "amount", "description"],
    [
        ("a" * 100, 1, 1, None),
        ("name", 0, 1, None),
        ("name", 1, -1, "desc"),
        ("name", 1, 1, "a" * 41),
    ],
)
def test_cart_item_invalid_args(
    name: str, quantity: int, amount: int, description: Optional[str]
):
    """Test for the invalid CartItem args."""
    with pytest.raises(ValueError):
        CartItem(name, quantity, amount, description)


def test_cart_as_json():
    """Test for the Cart.as_json()."""
    item = CartItem("example", 1, 1)
    assert Cart([item]).as_json() == [item.as_json()]
