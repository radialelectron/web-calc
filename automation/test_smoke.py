def test_backend_is_healthy(api):
    res = api.health()
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
