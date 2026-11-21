from . import router


def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


@router.get("/celsius-to-fahrenheit")
def convert_celsius_to_fahrenheit(value: float):
    return {
        "from": "celsius",
        "to": "fahrenheit",
        "value": value,
        "result": celsius_to_fahrenheit(value),
    }
