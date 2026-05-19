from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_register(client: TestClient, db: Session):
    r = client.post("/api/auth/register", json={"email": "newuser@example.com", "password": "password123"})
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "password" not in data

def test_register_duplicate_email(client: TestClient, test_user):
    r = client.post("/api/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert r.status_code == 400

def test_login(client: TestClient, test_user):
    r = client.post("/api/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "test@example.com"

def test_login_invalid_password(client: TestClient, test_user):
    r = client.post("/api/auth/login", json={"email": "test@example.com", "password": "wrongpassword"})
    assert r.status_code == 401

def test_login_nonexistent_user(client: TestClient):
    r = client.post("/api/auth/login", json={"email": "nobody@example.com", "password": "password"})
    assert r.status_code == 401
