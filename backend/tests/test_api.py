import uuid


def test_create(auth_client):
    r = auth_client.post("/api/todos", json={"title": "Buy groceries"})
    assert r.status_code == 201
    assert r.json()["title"] == "Buy groceries"
    assert r.json()["status"] == "pending"


def test_create_with_all_fields(auth_client):
    r = auth_client.post("/api/todos", json={
        "title": "Deploy app",
        "description": "Push to prod",
        "status": "in_progress",
        "due_date": "2025-06-01",
    })
    assert r.status_code == 201
    body = r.json()
    assert body["due_date"] == "2025-06-01"
    assert body["description"] == "Push to prod"


def test_create_rejects_blank_title(auth_client):
    assert auth_client.post("/api/todos", json={"title": "   "}).status_code == 422


def test_create_rejects_missing_title(auth_client):
    assert auth_client.post("/api/todos", json={}).status_code == 422


def test_get(auth_client):
    todo = auth_client.post("/api/todos", json={"title": "Test"}).json()
    r = auth_client.get(f"/api/todos/{todo['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test"


def test_get_returns_404(auth_client):
    assert auth_client.get(f"/api/todos/{uuid.uuid4()}").status_code == 404


def test_update(auth_client):
    todo = auth_client.post("/api/todos", json={"title": "Original"}).json()
    r = auth_client.patch(f"/api/todos/{todo['id']}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"


def test_partial_update_preserves_other_fields(auth_client):
    todo = auth_client.post("/api/todos", json={"title": "Task"}).json()
    r = auth_client.patch(f"/api/todos/{todo['id']}", json={"status": "completed"})
    assert r.json()["status"] == "completed"
    assert r.json()["title"] == "Task"


def test_delete(auth_client):
    todo = auth_client.post("/api/todos", json={"title": "Delete me"}).json()
    assert auth_client.delete(f"/api/todos/{todo['id']}").status_code == 204
    assert auth_client.get(f"/api/todos/{todo['id']}").status_code == 404


def test_delete_returns_404(auth_client):
    assert auth_client.delete(f"/api/todos/{uuid.uuid4()}").status_code == 404


def test_list_empty(auth_client):
    r = auth_client.get("/api/todos")
    assert r.json()["items"] == []
    assert r.json()["total"] == 0


def test_list_pagination(auth_client):
    for i in range(5):
        auth_client.post("/api/todos", json={"title": f"Task {i}"})

    r = auth_client.get("/api/todos", params={"page": 1, "page_size": 2})
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] == 5


def test_list_filter_by_status(auth_client):
    auth_client.post("/api/todos", json={"title": "A", "status": "pending"})
    auth_client.post("/api/todos", json={"title": "B", "status": "completed"})
    auth_client.post("/api/todos", json={"title": "C", "status": "completed"})

    r = auth_client.get("/api/todos", params={"status": "completed"})
    assert r.json()["total"] == 2
    assert all(t["status"] == "completed" for t in r.json()["items"])


def test_health(client):
    # health is unauthenticated
    assert client.get("/api/health").status_code == 200

def test_tenant_isolation(client, test_user):
    # Register a second user
    r = client.post("/api/auth/register", json={"email": "other@example.com", "password": "password"})
    assert r.status_code == 201
    
    # Login as second user
    r = client.post("/api/auth/login", json={"email": "other@example.com", "password": "password"})
    token2 = r.json()["access_token"]
    
    client.headers.update({"Authorization": f"Bearer {token2}"})
    
    # Create todo for user 2
    r = client.post("/api/todos", json={"title": "User 2 Todo"})
    todo2_id = r.json()["id"]
    
    # Login as user 1
    from app.auth import create_token
    token1 = create_token(test_user.id)
    client.headers.update({"Authorization": f"Bearer {token1}"})
    
    # User 1 cannot see User 2's todo
    assert client.get(f"/api/todos/{todo2_id}").status_code == 404
    
    # User 1 cannot delete User 2's todo
    assert client.delete(f"/api/todos/{todo2_id}").status_code == 404
