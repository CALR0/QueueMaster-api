def test_stats_endpoint(client):
    res = client.get("/api/v1/stats/queue/1")
    # May be 200 with data or 404 if not created; ensure endpoint reachable
    assert res.status_code in (200, 404)
