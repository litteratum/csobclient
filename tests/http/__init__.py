"""Test suites for http package."""
BASE_URL = "http://localhost"


def _build_url(endpoint: str = "index") -> str:
    return f"{BASE_URL}/{endpoint.lstrip('/')}"
