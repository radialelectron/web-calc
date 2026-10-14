from tip_calculator.webcalc_client import WebcalcClient


def tip_for_bill(client: WebcalcClient, bill: float, tip_percent: float) -> dict:
    """Tip amount and total for a bill, e.g. an 18% tip on 80.00."""
    tip = round(client.percent_of(bill, tip_percent), 2)
    total = round(client.add(bill, tip), 2)
    return {"bill": bill, "tip_percent": tip_percent, "tip": tip, "total": total}
