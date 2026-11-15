def _calculate(client, a, b, operator):
    res = client.post("/api/calculate", json={"a": a, "b": b, "operator": operator})
    assert res.status_code == 200


def test_clear_history_requires_confirmation(client):
    _calculate(client, 1, 2, "+")

    res = client.delete("/api/history")

    assert res.status_code == 400
    assert "confirm=true" in res.json()["detail"]
    assert len(client.get("/api/history").json()) == 1


def test_clear_history_with_confirmation_removes_everything(client):
    _calculate(client, 1, 2, "+")
    _calculate(client, 6, 3, "/")

    res = client.delete("/api/history", params={"confirm": "true"})

    assert res.status_code == 200
    assert res.json() == {"deleted": 2}
    assert client.get("/api/history").json() == []


def test_clearing_an_empty_history_deletes_nothing(client):
    res = client.delete("/api/history", params={"confirm": "true"})

    assert res.status_code == 200
    assert res.json() == {"deleted": 0}
