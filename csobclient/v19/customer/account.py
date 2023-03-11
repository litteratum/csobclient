"""Customer account."""
from typing import Optional
from ..fields import _IntField


class AccountData:
    """Customer account data."""

    order_history = _IntField(min_value=0, max_value=9999)
    payment_day = _IntField(min_value=0, max_value=999)
    payment_year = _IntField(min_value=0, max_value=999)
    oneclick_adds = _IntField(min_value=0, max_value=999)

    def __init__(
        self,
        created_at: Optional[str] = None,  # TODO: ISO8061
        changed_at: Optional[str] = None,  # TODO: ISO8061
        changed_pwd_at: Optional[str] = None,  # TODO: ISO8061
        order_history: Optional[int] = None,
        payment_day: Optional[int] = None,
        payment_year: Optional[int] = None,
        oneclick_adds: Optional[int] = None,
        suspicious: Optional[bool] = None,
    ) -> None:
        self.created_at = created_at
        self.changed_at = changed_at
        self.changed_pwd_at = changed_pwd_at
        self.order_history = order_history
        self.payment_day = payment_day
        self.payment_year = payment_year
        self.oneclick_adds = oneclick_adds
        self.suspicious = suspicious
