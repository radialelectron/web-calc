import json


def _calculate(client, a, b, operator):
    res = client.post("/api/calculate", json={"a": a, "b": b, "operator": operator})
    assert res.status_code == 200


def test_json_export_returns_count_and_items_in_order(client):
    _calculate(client, 1, 2, "+")
    _calculate(client, 6, 3, "/")

    res = client.get("/api/history/export.json")

    assert res.status_code == 200
    assert res.headers["content-type"].startswith("application/json")
    assert "history.json" in res.headers["content-disposition"]
    body = json.loads(res.text)
    assert body["count"] == 2
    assert [i["expression"] for i in body["items"]] == ["1.0 + 2.0", "6.0 / 3.0"]
    assert [i["result"] for i in body["items"]] == [3.0, 2.0]
    assert set(body["items"][0]) == {"id", "expression", "result", "mode", "created_at"}


def test_json_export_of_empty_history_has_zero_items(client):
    res = client.get("/api/history/export.json")

    assert res.status_code == 200
    assert json.loads(res.text) == {"count": 0, "items": []}
