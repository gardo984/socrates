from app.db.models import User
from app.core.security import hash_password


def test_list_users(client, auth_headers, session):
    session.add(User(name="User A", email="a@example.com", hashed_password=hash_password("pwd")))
    session.add(User(name="User B", email="b@example.com", hashed_password=hash_password("pwd")))
    session.commit()

    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    emails = [u["email"] for u in data]
    assert "a@example.com" in emails
    assert "b@example.com" in emails


def test_get_user_found(client, auth_headers, session):
    user = User(name="Target", email="target@example.com", hashed_password=hash_password("pwd"))
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.get(f"/users/{user.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "target@example.com"


def test_get_user_not_found(client, auth_headers):
    response = client.get("/users/9999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_success(client, auth_headers, session):
    payload = {"name": "Created", "email": "created@example.com", "password": "pwd"}
    response = client.post("/users/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "created@example.com"

    user_in_db = session.query(User).filter(User.email == "created@example.com").first()
    assert user_in_db is not None


def test_create_user_duplicate_email(client, auth_headers, session):
    session.add(User(name="Existing", email="dup@example.com", hashed_password=hash_password("pwd")))
    session.commit()

    payload = {"name": "Dup", "email": "dup@example.com", "password": "pwd"}
    response = client.post("/users/", json=payload, headers=auth_headers)
    assert response.status_code == 409


def test_update_user_success(client, auth_headers, session):
    user = User(name="Old Name", email="old@example.com", hashed_password=hash_password("pwd"))
    session.add(user)
    session.commit()
    session.refresh(user)

    payload = {"name": "New Name"}
    response = client.put(f"/users/{user.id}", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

    session.refresh(user)
    assert user.name == "New Name"


def test_update_user_partial(client, auth_headers, session):
    user = User(name="Partial", email="partial@example.com", hashed_password=hash_password("pwd"))
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.put(f"/users/{user.id}", json={"email": "updated@example.com"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"
    assert response.json()["name"] == "Partial"


def test_update_user_not_found(client, auth_headers):
    response = client.put("/users/9999", json={"name": "Nope"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_user_success(client, auth_headers, session):
    user = User(name="ToDelete", email="delete@example.com", hashed_password=hash_password("pwd"))
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.delete(f"/users/{user.id}", headers=auth_headers)
    assert response.status_code == 204

    assert session.query(User).filter(User.id == user.id).first() is None


def test_delete_user_not_found(client, auth_headers):
    response = client.delete("/users/9999", headers=auth_headers)
    assert response.status_code == 404
