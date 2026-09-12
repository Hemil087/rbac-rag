from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login(email: str, password: str) -> str:

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_documents_requires_authentication():

    response = client.get(
        "/api/v1/documents/"
    )

    assert response.status_code == 401


def test_invalid_token_is_rejected():

    response = client.get(
        "/api/v1/documents/",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_acme_employee_can_access_acme_document():

    token = login(
        "employee@acme.com",
        "employee123",
    )

    response = client.get(
        "/api/v1/documents/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    documents = response.json()

    filenames = [
        document["filename"]
        for document in documents
    ]

    assert "engineering_handbook.pdf" in filenames


def test_globex_employee_can_access_globex_document():

    token = login(
        "employee@globex.com",
        "employee123",
    )

    response = client.get(
        "/api/v1/documents/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    documents = response.json()

    filenames = [
        document["filename"]
        for document in documents
    ]

    assert "globex_hr_policy.pdf" in filenames


def test_acme_employee_cannot_access_globex_document():

    token = login(
        "employee@acme.com",
        "employee123",
    )

    response = client.get(
        "/api/v1/documents/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    documents = response.json()

    filenames = [
        document["filename"]
        for document in documents
    ]

    assert "globex_hr_policy.pdf" not in filenames


def test_globex_employee_cannot_access_acme_document():

    token = login(
        "employee@globex.com",
        "employee123",
    )

    response = client.get(
        "/api/v1/documents/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    documents = response.json()

    filenames = [
        document["filename"]
        for document in documents
    ]

    assert "engineering_handbook.pdf" not in filenames

def test_me_returns_jwt_user_context():

    token = login(
        "employee@acme.com",
        "employee123",
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 3
    assert data["org_id"] == 1
    assert data["role_id"] == 3