import csv
import io


def _calculate(client, a, b, operator):
    res = client.post("/api/calculate", json={"a": a, "b": b, "operator": operator})
    assert res.status_code == 200


def test_csv_export_returns_header_and_rows_in_order(client):
    _calculate(client, 1, 2, "+")
    _calculate(client, 6, 3, "/")

    res = client.get("/api/history/export.csv")

    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/csv")
    assert "history.csv" in res.headers["content-disposition"]
    rows = list(csv.reader(io.StringIO(res.text)))
    assert rows[0] == ["id", "expression", "result", "mode", "created_at"]
    assert [r[1] for r in rows[1:]] == ["1.0 + 2.0", "6.0 / 3.0"]
    assert [r[2] for r in rows[1:]] == ["3.0", "2.0"]


def test_csv_export_of_empty_history_is_header_only(client):
    res = client.get("/api/history/export.csv")

    assert res.status_code == 200
    rows = list(csv.reader(io.StringIO(res.text)))
    assert rows == [["id", "expression", "result", "mode", "created_at"]]
