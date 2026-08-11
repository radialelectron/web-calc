import pytest


@pytest.mark.parametrize(
    "function,value,angle_mode,expected",
    [
        ("sin", 30, "deg", 0.5),
        ("cos", 60, "deg", 0.5),
        ("sqrt", 16, "deg", 4),
        ("log", 100, "deg", 2),
    ],
)
def test_scientific_functions(client, function, value, angle_mode, expected):
    res = client.post(
        "/api/calculate/scientific",
        json={"function": function, "value": value, "angle_mode": angle_mode},
    )
    assert res.status_code == 200
    assert round(res.json()["result"], 4) == expected


def test_trig_radian_mode(client):
    import math

    res = client.post(
        "/api/calculate/scientific",
        json={"function": "sin", "value": math.pi / 2, "angle_mode": "rad"},
    )
    assert res.status_code == 200
    assert round(res.json()["result"], 4) == 1.0


def test_pow_function(client):
    res = client.post(
        "/api/calculate/scientific",
        json={"function": "pow", "value": 2, "angle_mode": "deg", "exponent": 5},
    )
    assert res.status_code == 200
    assert res.json()["result"] == 32


def test_log_of_negative_number_returns_400(client):
    res = client.post(
        "/api/calculate/scientific",
        json={"function": "log", "value": -5, "angle_mode": "deg"},
    )
    assert res.status_code == 400


def test_sqrt_of_negative_number_returns_400(client):
    res = client.post(
        "/api/calculate/scientific",
        json={"function": "sqrt", "value": -9, "angle_mode": "deg"},
    )
    assert res.status_code == 400


def test_pow_without_exponent_returns_400(client):
    res = client.post(
        "/api/calculate/scientific",
        json={"function": "pow", "value": 2, "angle_mode": "deg"},
    )
    assert res.status_code == 400


def test_scientific_calculation_persisted_with_function_type(client):
    client.post(
        "/api/calculate/scientific",
        json={"function": "cos", "value": 0, "angle_mode": "deg"},
    )
    res = client.get("/api/history")
    entries = res.json()
    assert any(e["function_type"] == "cos" and e["mode"] == "scientific" for e in entries)
