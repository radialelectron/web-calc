from tip_calculator.tip import tip_for_bill


def test_eighteen_percent_tip_on_80(webcalc):
    assert tip_for_bill(webcalc, 80, 18) == {
        "bill": 80,
        "tip_percent": 18,
        "tip": 14.4,
        "total": 94.4,
    }


def test_zero_tip(webcalc):
    assert tip_for_bill(webcalc, 50, 0)["total"] == 50


def test_percent_of_matches_documented_semantics(webcalc):
    assert webcalc.percent_of(200, 10) == 20
