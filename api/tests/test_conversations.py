from app.db.models import Document, Conversation, Message, User
from app.core.security import hash_password


# ---- Conversation tests ----


def test_create_conversation_success(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    payload = {"document_id": doc.id, "title": "My Conversation"}
    response = client.post("/conversations/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Conversation"
    assert data["document_id"] == doc.id


def test_create_conversation_document_not_found(client, auth_headers):
    payload = {"document_id": 9999, "title": "Orphan"}
    response = client.post("/conversations/", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_list_conversations(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    session.add(Conversation(document_id=doc.id, title="Conv 1"))
    session.add(Conversation(document_id=doc.id, title="Conv 2"))
    session.commit()

    response = client.get("/conversations/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    titles = [c["title"] for c in data]
    assert "Conv 1" in titles
    assert "Conv 2" in titles


def test_get_conversation_found(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Target Conv")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    response = client.get(f"/conversations/{conv.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Target Conv"


def test_get_conversation_not_found(client, auth_headers):
    response = client.get("/conversations/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_conversation(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Old Title")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    response = client.put(
        f"/conversations/{conv.id}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_update_conversation_not_found(client, auth_headers):
    response = client.put("/conversations/9999", json={"title": "Nope"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_conversation(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="To Delete")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    response = client.delete(f"/conversations/{conv.id}", headers=auth_headers)
    assert response.status_code == 204

    assert session.query(Conversation).filter(Conversation.id == conv.id).first() is None


def test_delete_conversation_not_found(client, auth_headers):
    response = client.delete("/conversations/9999", headers=auth_headers)
    assert response.status_code == 404


def test_get_document_conversations(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    session.add(Conversation(document_id=doc.id, title="Conv A"))
    session.add(Conversation(document_id=doc.id, title="Conv B"))
    session.commit()

    response = client.get(f"/documents/{doc.id}/conversations", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_document_conversations_doc_not_found(client, auth_headers):
    response = client.get("/documents/9999/conversations", headers=auth_headers)
    assert response.status_code == 404


# ---- Message tests ----


def test_create_message_success(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Conv")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    payload = {"conversation_id": conv.id, "role": "user", "content": "Hello world"}
    response = client.post(
        f"/conversations/{conv.id}/messages",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "user"
    assert data["content"] == "Hello world"
    assert data["conversation_id"] == conv.id


def test_create_message_conversation_not_found(client, auth_headers):
    payload = {"conversation_id": 9999, "role": "user", "content": "Hello"}
    response = client.post("/conversations/9999/messages", json=payload, headers=auth_headers)
    assert response.status_code == 404


def test_list_messages(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Conv")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    session.add(Message(conversation_id=conv.id, role="user", content="Msg 1"))
    session.add(Message(conversation_id=conv.id, role="assistant", content="Msg 2"))
    session.commit()

    response = client.get(f"/conversations/{conv.id}/messages", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_messages_conversation_not_found(client, auth_headers):
    response = client.get("/conversations/9999/messages", headers=auth_headers)
    assert response.status_code == 404


def test_get_message_found(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Conv")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    msg = Message(conversation_id=conv.id, role="user", content="Target msg")
    session.add(msg)
    session.commit()
    session.refresh(msg)

    response = client.get(f"/messages/{msg.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["content"] == "Target msg"


def test_get_message_not_found(client, auth_headers):
    response = client.get("/messages/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_message(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Conv")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    msg = Message(conversation_id=conv.id, role="user", content="Old content")
    session.add(msg)
    session.commit()
    session.refresh(msg)

    response = client.put(
        f"/messages/{msg.id}",
        json={"content": "New content"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["content"] == "New content"


def test_update_message_not_found(client, auth_headers):
    response = client.put("/messages/9999", json={"content": "Nope"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_message(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="doc.txt", file_type="txt", file_size=100, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    conv = Conversation(document_id=doc.id, title="Conv")
    session.add(conv)
    session.commit()
    session.refresh(conv)

    msg = Message(conversation_id=conv.id, role="user", content="To delete")
    session.add(msg)
    session.commit()
    session.refresh(msg)

    response = client.delete(f"/messages/{msg.id}", headers=auth_headers)
    assert response.status_code == 204

    assert session.query(Message).filter(Message.id == msg.id).first() is None


def test_delete_message_not_found(client, auth_headers):
    response = client.delete("/messages/9999", headers=auth_headers)
    assert response.status_code == 404
