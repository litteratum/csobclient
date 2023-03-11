"""Merchant models."""
from base64 import b64encode
from typing import Optional


class _MerchantData:
    """Merchant data."""

    def __init__(self, data: Optional[bytes]) -> None:
        self._data = data

    @property
    def value(self) -> Optional[str]:
        """Return merchant data as string."""
        if self._data is None:
            return None

        data = b64encode(self._data).decode("UTF-8")
        if len(data) > 255:
            raise ValueError(
                "Merchant data length encoded to BASE64 is over 255 chars"
            )

        return data
