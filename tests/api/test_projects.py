import os

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.mark.skipif(os.getenv("RUN_DB_TESTS") != "true", reason="Database tests disabled")
def test_list_projects_requires_db():
    os.environ["AUTH_DISABLED"] = "true"
    client = TestClient(app)
    response = client.get("/api/projects/")
    assert response.status_code == 200
