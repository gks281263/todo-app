import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSession = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def _reset_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    s = TestSession()
    try:
        yield s
    finally:
        s.close()


@pytest.fixture
def client(db):
    def override():
        yield db

    app.dependency_overrides[get_db] = override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    from app.auth import hash_pw
    from app.models import User
    
    u = User(email="test@example.com", password_hash=hash_pw("password123"))
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@pytest.fixture
def auth_client(client, test_user):
    from app.auth import create_token
    token = create_token(test_user.id)
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
