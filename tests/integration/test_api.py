from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready(client: TestClient):
    response = client.get("/ready")
    assert response.status_code == 200


def test_documents(client: TestClient):
    response = client.get("/v1/documents")
    assert response.status_code in [200, 401, 403, 422]


def test_list_documents_returns_records(client: TestClient):
    response = client.get("/v1/documents")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data


def test_list_documents_limit(client: TestClient):
    response = client.get("/v1/documents?limit=5")
    assert response.status_code == 200
    assert len(response.json()["items"]) <= 5


def test_list_documents_offset(client: TestClient):
    response = client.get("/v1/documents?offset=2")
    assert response.status_code == 200
    assert response.json()["offset"] == 2


def test_search_documents(client: TestClient):
    response = client.get("/v1/documents?q=Aarav")
    assert response.status_code == 200
    assert "items" in response.json()


def test_get_existing_document(client: TestClient):
    response = client.get("/v1/documents/PP001")
    assert response.status_code == 200
    assert response.json()["id"] == "PP001"


def test_get_missing_document(client: TestClient):
    response = client.get("/v1/documents/INVALID")
    assert response.status_code == 404


def test_invalid_limit(client: TestClient):
    response = client.get("/v1/documents?limit=0")
    assert response.status_code == 422
