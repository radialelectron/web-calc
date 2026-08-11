"""Automates TC-01..TC-07 from the Confluence Test Cases page (standard calculator)."""
import pytest


@pytest.mark.parametrize(
    "test_id,a,b,operator,expected",
    [
        ("TC-01", 2, 3, "+", 5),
        ("TC-02", 2, 5, "-", -3),
        ("TC-03", 4, 5, "*", 20),
        ("TC-04", 10, 2, "/", 5),
        ("TC-06", 200, 10, "%", 20),
    ],
)
def test_arithmetic_operations(api, test_id, a, b, operator, expected):
    res = api.calculate(a, b, operator)
    assert res.status_code == 200, test_id
    assert res.json()["result"] == expected, test_id


def test_tc05_divide_by_zero(api):
    res = api.calculate(5, 0, "/")
    assert res.status_code == 400
    assert "Cannot divide by zero" in res.json()["detail"]


def test_tc07_calculation_persisted_to_history(api):
    res = api.calculate(9, 6, "+")
    assert res.status_code == 200

    history_res = api.history()
    assert history_res.status_code == 200
    entries = history_res.json()
    assert any(e["expression"] == "9.0 + 6.0" and e["result"] == 15 for e in entries)
