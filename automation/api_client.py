import requests

from config import BASE_URL, TIMEOUT


class WebCalcClient:
    """Thin HTTP client for the WEB Calc API, used by all automated test suites."""

    def __init__(self, base_url: str = BASE_URL, timeout: float = TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout

    def health(self):
        return requests.get(f"{self.base_url}/api/health", timeout=self.timeout)

    def calculate(self, a, b, operator):
        return requests.post(
            f"{self.base_url}/api/calculate",
            json={"a": a, "b": b, "operator": operator},
            timeout=self.timeout,
        )

    def calculate_scientific(self, function, value, angle_mode="deg", exponent=None):
        payload = {"function": function, "value": value, "angle_mode": angle_mode}
        if exponent is not None:
            payload["exponent"] = exponent
        return requests.post(
            f"{self.base_url}/api/calculate/scientific",
            json=payload,
            timeout=self.timeout,
        )

    def history(self, limit=50):
        return requests.get(
            f"{self.base_url}/api/history",
            params={"limit": limit},
            timeout=self.timeout,
        )
