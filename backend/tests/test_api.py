import uuid


def test_create(client):
    r = client.post("/api/todos", json={"title": "Buy groceries"})
    assert r.status_code == 201
    assert r.json()["title"] == "Buy groceries"
    assert r.json()["status"] == "pending"


def test_create_with_all_fields(client):
    r = client.post("/api/todos", json={
        "title": "Deploy app",
        "description": "Push to prod",
        "status": "in_progress",
        "due_date": "2025-06-01",
    })
    assert r.status_code == 201
    body = r.json()
    assert body["due_date"] == "2025-06-01"
    assert body["description"] == "Push to prod"


def test_create_rejects_blank_title(client):
    assert client.post("/api/todos", json={"title": "   "}).status_code == 422


def test_create_rejects_missing_title(client):
    assert client.post("/api/todos", json={}).status_code == 422


def test_get(client):
    todo = client.post("/api/todos", json={"title": "Test"}).json()
    r = client.get(f"/api/todos/{todo['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test"


def test_get_returns_404(client):
    assert client.get(f"/api/todos/{uuid.uuid4()}").status_code == 404


def test_update(client):
    todo = client.post("/api/todos", json={"title": "Original"}).json()
    r = client.patch(f"/api/todos/{todo['id']}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"


def test_partial_update_preserves_other_fields(client):
    todo = client.post("/api/todos", json={"title": "Task"}).json()
    r = client.patch(f"/api/todos/{todo['id']}", json={"status": "completed"})
    assert r.json()["status"] == "completed"
    assert r.json()["title"] == "Task"


def test_delete(client):
    todo = client.post("/api/todos", json={"title": "Delete me"}).json()
    assert client.delete(f"/api/todos/{todo['id']}").status_code == 204
    assert client.get(f"/api/todos/{todo['id']}").status_code == 404


def test_delete_returns_404(client):
    assert client.delete(f"/api/todos/{uuid.uuid4()}").status_code == 404


def test_list_empty(client):
    r = client.get("/api/todos")
    assert r.json()["items"] == []
    assert r.json()["total"] == 0


def test_list_pagination(client):
    for i in range(5):
        client.post("/api/todos", json={"title": f"Task {i}"})

    r = client.get("/api/todos", params={"page": 1, "page_size": 2})
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] == 5


def test_list_filter_by_status(client):
    client.post("/api/todos", json={"title": "A", "status": "pending"})
    client.post("/api/todos", json={"title": "B", "status": "completed"})
    client.post("/api/todos", json={"title": "C", "status": "completed"})

    r = client.get("/api/todos", params={"status": "completed"})
    assert r.json()["total"] == 2
    assert all(t["status"] == "completed" for t in r.json()["items"])


def test_health(client):
    assert client.get("/api/health").status_code == 200
