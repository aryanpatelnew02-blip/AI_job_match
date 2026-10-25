from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.app.db.database import get_db
from backend.app.main import app


def test_health_endpoint_healthy(client: TestClient):
    """Verify /api/v1/health returns 200 and healthy payload when DB and pgvector are available."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["pgvector"]["status"] == "installed"
    assert data["pgvector"]["version"] == "0.7.0"
    assert "timestamp" in data
    assert "X-Request-ID" in response.headers


def test_health_endpoint_db_failure():
    """Verify /api/v1/health returns 503 when the database is unreachable."""
    failing_db = MagicMock()
    failing_db.execute.side_effect = Exception("Connection refused")

    app.dependency_overrides[get_db] = lambda: failing_db
    try:
        with TestClient(app) as local_client:
            response = local_client.get("/api/v1/health")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["database"] == "disconnected"
            assert "Database error" in str(data.get("errors", []))
    finally:
        app.dependency_overrides.clear()


def test_request_id_middleware(client: TestClient):
    """Verify incoming X-Request-ID is preserved in response headers."""
    custom_req_id = "test-req-12345"
    response = client.get("/api/v1/health", headers={"X-Request-ID": custom_req_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_req_id
    assert "X-Process-Time-Ms" in response.headers
