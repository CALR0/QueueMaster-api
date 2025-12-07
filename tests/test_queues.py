def test_queue_crud(client):
    # Create
    res = client.post("/api/v1/queues/", json={"name": "Test Queue", "description": "desc"})
    assert res.status_code == 200
    data = res.json()
    qid = data["id"] if isinstance(data, dict) and "id" in data else data.get("id")
    assert data["name"] == "Test Queue"

    # Read
    res = client.get(f"/api/v1/queues/{qid}")
    assert res.status_code == 200

    # Update
    res = client.put(f"/api/v1/queues/{qid}", json={"description": "new"})
    assert res.status_code == 200

    # Delete
    res = client.delete(f"/api/v1/queues/{qid}")
    assert res.status_code == 200
