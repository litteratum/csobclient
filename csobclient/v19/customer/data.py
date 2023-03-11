"""Customer data."""
from typing import Optional

from .account import AccountData
from .login import LoginData
from ..fields import _StrField


class PhoneNumber:
    """Phone number."""

    def __init__(self, prefix: str, subscriber: str) -> None:
        self.prefix = prefix
        self.subscriber = subscriber


class CustomerData:
    """Customer information."""

    name = _StrField(max_length=45)
    email = _StrField(max_length=100)

    def __init__(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        home_phone: Optional[PhoneNumber] = None,
        work_phone: Optional[PhoneNumber] = None,
        mobile_phone: Optional[PhoneNumber] = None,
        account: Optional[AccountData] = None,
        login: Optional[LoginData] = None,
    ) -> None:
        self.name = name
        self.email = email
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.mobile_phone = mobile_phone
        self.account = account
        self.login = login
