"""Module for dealing with the signature."""
from base64 import b64decode, b64encode
from collections import OrderedDict
from .dttm import decode_dttm

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


_RESPONSE_KEYS = (
    "payId",
    "customerId",
    "dttm",
    "resultCode",
    "resultMessage",
    "paymentStatus",
    "authCode",
    "merchantData",
)


class InvalidSignatureError(Exception):
    """Response signature is invalid."""


def str_or_jsbool(v):
    if type(v) == bool:
        return str(v).lower()
    return str(v)


def mk_msg_for_sign(payload):
    payload = payload.copy()
    if payload.get("cart"):
        cart_msg = []
        for one in payload["cart"]:
            cart_msg.extend(one.values())
        payload["cart"] = "|".join(map(str_or_jsbool, cart_msg))
    msg = "|".join(map(str_or_jsbool, payload.values()))
    return msg.encode("utf-8")


def sign(payload, keyfile):
    msg = mk_msg_for_sign(payload)
    key = RSA.importKey(open(keyfile).read())
    h = SHA256.new(msg)
    signer = PKCS1_v1_5.new(key)
    return b64encode(signer.sign(h)).decode()


def _verify(payload: dict, signature: str, pubkeyfile: str):
    msg = mk_msg_for_sign(payload)
    key = RSA.importKey(open(pubkeyfile).read())
    h = SHA256.new(msg)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, b64decode(signature))


def verify(json_data: dict, key) -> OrderedDict:
    """Verify data signature."""
    signature = json_data.pop("signature", None)
    if not signature:
        raise InvalidSignatureError("Empty signature")

    payload = OrderedDict()
    for k in _RESPONSE_KEYS:
        if k in json_data:
            payload[k] = json_data[k]

    if not _verify(payload, signature, key):
        raise InvalidSignatureError("Invalid signature")

    if "dttm" in payload:
        payload["dttime"] = decode_dttm(payload["dttm"])

    return payload
