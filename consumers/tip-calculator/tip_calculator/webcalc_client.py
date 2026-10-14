import httpx
from tip_calculator.config import WEBCALC_BASE_URL


class WebcalcClient:
    """Thin client for Webcalc POST /api/calculate."""

    def __init__(self, http: httpx.Client | None = None):
        self._http = http or httpx.Client(base_url=WEBCALC_BASE_URL)

    def percent_of(self, amount: float, percent: float) -> float:
        """Webcalc operator '%': `percent` percent of `amount`."""
        return self._calculate(amount, percent, "%")

    def add(self, a: float, b: float) -> float:
        return self._calculate(a, b, "+")

    def _calculate(self, a: float, b: float, operator: str) -> float:
        res = self._http.post(
            "/api/calculate", json={"a": a, "b": b, "operator": operator}
        )
        res.raise_for_status()
        return res.json()["result"]
