import pytest
from fastapi.testclient import TestClient
from src import app


@pytest.fixture
def client():
    return TestClient(app)

def test_heartbeat(client):
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert response.json() == "hi"
