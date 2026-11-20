from . import router


def kilometres_to_metres(kilometres: float) -> float:
    # DEMO DEFECT (S2, intentional): the correct factor is 1000.
    return kilometres * 100


@router.get("/km-to-metres")
def convert_km_to_metres(value: float):
    return {
        "from": "kilometres",
        "to": "metres",
        "value": value,
        "result": kilometres_to_metres(value),
    }
