"""Checks the assumptions tip_calculator makes against the committed Webcalc contract."""

import json
import os

from tip_calculator.config import WEBCALC_CONTRACT

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")


def _spec():
    with open(os.path.join(ROOT, WEBCALC_CONTRACT)) as f:
        return json.load(f)


def test_calculate_operation_exists():
    assert "post" in _spec()["paths"]["/api/calculate"]


def test_percent_operator_means_b_percent_of_a():
    operator = _spec()["components"]["schemas"]["CalculateRequest"]["properties"][
        "operator"
    ]
    assert "b percent of a" in operator["description"]


def test_response_result_is_a_number():
    result = _spec()["components"]["schemas"]["CalculateResponse"]["properties"][
        "result"
    ]
    assert result["type"] == "number"
