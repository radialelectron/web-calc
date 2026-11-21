def test_one_kilometre_converts_to_1000_metres(client):
    res = client.get("/api/convert/km-to-metres", params={"value": 1})

    assert res.status_code == 200
    assert res.json()["result"] == 1000
