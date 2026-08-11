import pytest


@pytest.mark.parametrize(
    "a,b,operator,expected",
    [
        (2, 3, "+", 5),
        (2, 5, "-", -3),
        (4, 5, "*", 20),
        (10, 2, "/", 5),
        (200, 10, "%", 20),
    ],
)
def test_arithmetic_operations(client, a, b, operator, expected):
    res = client.post("/api/calculate", json={"a": a, "b": b, "operator": operator})
    assert res.status_code == 200
    assert res.json()["result"] == expected


def test_divide_by_zero_returns_400(client):
    res = client.post("/api/calculate", json={"a": 5, "b": 0, "operator": "/"})
    assert res.status_code == 400
    assert "Cannot divide by zero" in res.json()["detail"]


def test_unsupported_operator_returns_400(client):
    res = client.post("/api/calculate", json={"a": 1, "b": 1, "operator": "^"})
    assert res.status_code == 400


def test_calculation_is_persisted_to_history(client):
    client.post("/api/calculate", json={"a": 7, "b": 8, "operator": "+"})
    res = client.get("/api/history")
    assert res.status_code == 200
    entries = res.json()
    assert any(e["expression"] == "7.0 + 8.0" and e["result"] == 15 for e in entries)
