from fastapi.testclient import TestClient
from src.routes.run import app, invoke

client = TestClient(app)

def test_invoke_success():
    response = client.post(
        "/invoke/success_node",
        json={
            "messages": [
                {"content": "Hello, world!", "role": "user"},
                {"content": "Hello, user!", "role": "assistant"},
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}

def test_invoke_error():
    response = client.post(
        "/invoke/error_node",
        json={
            "messages": [
                {"content": "Hello, world!", "role": "user"},
                {"content": "Hello, user!", "role": "assistant"},
            ]
        },
    )
    assert response.status_code == 500
    assert "error" in response.text

def test_invoke_edge_case():
    response = client.post(
        "/invoke/edge_case_node",
        json={
            "messages": [
                {"content": "Edge case message", "role": "user"},
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Edge case handled"}
