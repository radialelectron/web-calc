"""Automates TC-11..TC-16 from the Confluence Test Cases page (scientific calculator)."""
import pytest


@pytest.mark.parametrize(
    "test_id,function,value,angle_mode,expected",
    [
        ("TC-11", "sin", 30, "deg", 0.5),
        ("TC-12", "cos", 60, "deg", 0.5),
        ("TC-13", "log", 100, "deg", 2),
        ("TC-14", "sqrt", 16, "deg", 4),
    ],
)
def test_scientific_functions(api, test_id, function, value, angle_mode, expected):
    res = api.calculate_scientific(function, value, angle_mode)
    assert res.status_code == 200, test_id
    assert round(res.json()["result"], 4) == expected, test_id


def test_tc15_log_of_negative_number_returns_error(api):
    res = api.calculate_scientific("log", -5, "deg")
    assert res.status_code == 400


def test_tc16_degree_and_radian_mode_differ(api):
    import math

    deg_res = api.calculate_scientific("sin", 90, "deg")
    rad_res = api.calculate_scientific("sin", 90, "rad")

    assert round(deg_res.json()["result"], 4) == 1.0
    assert round(rad_res.json()["result"], 4) == round(math.sin(90), 4)
