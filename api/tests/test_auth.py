from app.db.models import User
from app.core.security import hash_password


def test_register_success(client, session):
    payload = {"name": "New User", "email": "new@example.com", "password": "secret123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New User"
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "password" not in data

    user_in_db = session.query(User).filter(User.email == "new@example.com").first()
    assert user_in_db is not None


def test_register_duplicate_email(client, session):
    session.add(User(name="Existing", email="dup@example.com", hashed_password=hash_password("pwd")))
    session.commit()

    payload = {"name": "Dup", "email": "dup@example.com", "password": "pwd"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client, session):
    session.add(User(
        name="Login User",
        email="login@example.com",
        hashed_password=hash_password("correct_password"),
    ))
    session.commit()

    payload = {"email": "login@example.com", "password": "correct_password"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, session):
    session.add(User(
        name="Login User",
        email="login@example.com",
        hashed_password=hash_password("correct_password"),
    ))
    session.commit()

    payload = {"email": "login@example.com", "password": "wrong_password"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401


def test_login_unknown_email(client, session):
    payload = {"email": "unknown@example.com", "password": "any"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
