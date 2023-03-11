"""Tests for the client."""
import csobclient
import pytest

_CLIENT = csobclient.Client("id", "url", "pvk", "pk")


@pytest.mark.parametrize(
    ["ttl_sec"],
    [
        (0,),
        (-1,),
        (299,),
        (1801,),
    ],
)
def test_init_payment_invalid_ttl_sec(ttl_sec: int):
    """Test for the invalid ttl_sec values."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment(
            "order_no", 100, "http://127.0.0.1", ttl_sec=ttl_sec
        )


def test_init_payment_invalid_order_no():
    """Test for the invalid order_no value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment("1" * 11, 100, "http://127.0.0.1")


def test_init_payment_invalid_return_url():
    """Test for the invalid return_url value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment("123", 100, "a" * 301)


def test_init_payment_invalid_customer_id():
    """Test for the invalid customer_id value."""
    with pytest.raises(ValueError):
        _CLIENT.init_payment(
            "123", 100, "http://127.0.0.1", customer_id="a" * 51
        )
