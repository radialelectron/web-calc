def test_zero_celsius_converts_to_32_fahrenheit(client):
    res = client.get("/api/convert/celsius-to-fahrenheit", params={"value": 0})

    assert res.status_code == 200
    assert res.json()["result"] == 32


def test_100_celsius_converts_to_212_fahrenheit(client):
    res = client.get("/api/convert/celsius-to-fahrenheit", params={"value": 100})

    assert res.status_code == 200
    assert res.json()["result"] == 212
