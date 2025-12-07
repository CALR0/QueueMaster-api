def test_notifications(client):
    payload = {"to": "user@example.com", "subject": "Hi", "message": "Hello", "channel": "email"}
    res = client.post("/api/v1/notifications/send", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
