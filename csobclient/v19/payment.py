"""Payment models."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PaymentOperation(Enum):
    """Payment operation."""

    PAYMENT = "payment"
    ONE_CLICK_PAYMENT = "oneclickPayment"
    CUSTOM_PAYMENT = "customPayment"


class PaymentMethod(Enum):
    """Payment method."""

    CARD = "card"
    CARD_LVP = "card#LVP"


@dataclass(frozen=True)
class PaymentInitInfo:
    """Payment information."""

    pay_id: str
    payment_status: Optional[int]
    customer_code: Optional[str]
