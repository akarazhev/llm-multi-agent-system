import os

from fastapi.testclient import TestClient

from src.api.main import app


def test_health_check():
    os.environ["AUTH_DISABLED"] = "true"
    client = TestClient(app)
    response = client.get("/api/health/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
