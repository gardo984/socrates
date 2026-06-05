import io
import os

from app.db.models import Document, User
from app.core.security import hash_password


def test_list_documents(client, auth_headers, session):
    user = session.query(User).first()
    session.add(Document(filename="doc1.txt", file_type="txt", file_size=100, user_id=user.id))
    session.add(Document(filename="doc2.pdf", file_type="pdf", file_size=200, user_id=user.id))
    session.commit()

    response = client.get("/documents/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    filenames = [d["filename"] for d in data]
    assert "doc1.txt" in filenames
    assert "doc2.pdf" in filenames


def test_get_document_found(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="found.txt", file_type="txt", file_size=50, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    response = client.get(f"/documents/{doc.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["filename"] == "found.txt"


def test_get_document_not_found(client, auth_headers):
    response = client.get("/documents/9999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_upload_document_txt(client, auth_headers, session):
    content = b"Hello, this is a test document."
    file_obj = io.BytesIO(content)
    response = client.post(
        "/documents/upload",
        files={"file": ("test.txt", file_obj, "text/plain")},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["file_type"] == "txt"
    assert data["file_size"] == len(content)

    # Clean up uploaded file
    file_path = os.path.join("uploads", "test.txt")
    if os.path.exists(file_path):
        os.remove(file_path)


def test_upload_document_unsupported_type(client, auth_headers):
    file_obj = io.BytesIO(b"some content")
    response = client.post(
        "/documents/upload",
        files={"file": ("test.exe", file_obj, "application/x-msdownload")},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_delete_document_success(client, auth_headers, session):
    user = session.query(User).first()
    doc = Document(filename="deleteme.txt", file_type="txt", file_size=10, user_id=user.id)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    # Create a dummy upload file to ensure cleanup path is tested
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", "deleteme.txt")
    with open(file_path, "w") as f:
        f.write("content")

    response = client.delete(f"/documents/{doc.id}", headers=auth_headers)
    assert response.status_code == 204
    assert os.path.exists(file_path) is False

    # Verify DB record is gone
    assert session.query(Document).filter(Document.id == doc.id).first() is None


def test_delete_document_not_found(client, auth_headers):
    response = client.delete("/documents/9999", headers=auth_headers)
    assert response.status_code == 404
