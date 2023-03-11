"""Client."""
from collections import OrderedDict
from enum import Enum
from typing import Optional

from .currency import Currency
from .customer import CustomerData
from .order import OrderData
from .payment import PaymentMethod, PaymentOperation, PaymentInitInfo
from .cart import Cart, CartItem
from .merchant import _MerchantData
from .webpage import WebPageAppearanceConfig
from .dttm import get_dttm, get_payment_expiry
from .signature import sign
from .http import RequestsHTTPClient


class ReturnMethod(Enum):
    """Return method."""

    POST = "POST"
    GET = "GET"


class APIError(Exception):
    """API error."""

    def __init__(
        self, code: int, message: str, status_detail: Optional[str] = None
    ) -> None:
        """Init API error.

        :param code: error code
        :message: error message
        :status_detail: status detail
        """
        message = f"{code}: {message}"
        if status_detail:
            message = f"{message}. Details: {status_detail}"

        super().__init__(message)


class Client:
    """API client."""

    def __init__(
        self,
        merchant_id: str,
        base_url: str,
        private_key_file: str,
        csob_public_key_file: str,
    ) -> None:
        self.merchant_id = merchant_id
        self.base_url = base_url.rstrip("/")
        self.private_key_file = private_key_file
        self.csob_public_key_file = csob_public_key_file

        self._http_client = RequestsHTTPClient()

    def _mk_payload(self, pairs):
        payload = OrderedDict([(k, v) for k, v in pairs if v])
        payload["signature"] = sign(payload, self.private_key_file)
        return payload

    def init_payment(
        self,
        order_no: str,
        total_amount: int,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        payment_operation: PaymentOperation = PaymentOperation.PAYMENT,
        payment_method: PaymentMethod = PaymentMethod.CARD,
        currency: Currency = Currency.CZK,
        close_payment: bool = True,
        ttl_sec: int = 600,
        cart: Optional[Cart] = None,
        customer: Optional[CustomerData] = None,
        order: Optional[OrderData] = None,
        merchant_data: Optional[bytes] = None,
        customer_id: Optional[str] = None,
        payment_expiry: Optional[int] = None,
        page_appearance: WebPageAppearanceConfig = WebPageAppearanceConfig(),
    ) -> PaymentInitInfo:
        """Init payment."""
        if not (300 <= ttl_sec <= 1800):
            raise ValueError('"ttl_sec" must be in [300, 1800]')
        if len(order_no) > 10:
            raise ValueError('"order_no" must be up to 10 chars')
        if len(return_url) > 300:
            raise ValueError('"return_url" must be up to 300 chars')
        if customer_id and len(customer_id) > 50:
            raise ValueError('"customer_id" must be up to 50 chars')

        cart = cart or Cart([CartItem("Payment", 1, total_amount)])

        payload = self._mk_payload(
            pairs=(
                ("merchantId", self.merchant_id),
                ("orderNo", order_no),
                ("dttm", get_dttm()),
                ("payOperation", payment_operation.value),
                ("payMethod", payment_method.value),
                ("totalAmount", total_amount),
                ("currency", currency.value),
                ("closePayment", close_payment),
                ("returnUrl", return_url),
                ("returnMethod", return_method.value),
                ("cart", cart.as_json()),
                ("customer", customer),  # TODO: add as_json()
                ("order", order),  # TODO: add as_json()
                ("merchantData", _MerchantData(merchant_data).value),
                ("customerId", customer_id),
                ("language", page_appearance.language.value),
                ("ttlSec", ttl_sec),
                ("logoVersion", page_appearance.logo_version),
                ("colorSchemeVersion", page_appearance.color_scheme_version),
                ("customExpiry", get_payment_expiry(payment_expiry)),
            ),
        )
        response = self._http_client.post_json(
            f"{self.base_url}/payment/init", payload
        )

        # TODO: validate response

        if response.http_success and response.data["resultCode"] == 0:
            return PaymentInitInfo(
                response.data["payId"],
                response.data.get("paymentStatus"),
                response.data.get("customerCode"),
            )

        raise APIError(
            response.data["resultCode"],
            response.data["resultMessage"],
            response.data.get("statusDetail"),
        )
