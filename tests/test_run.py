from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from src.routes.run import Context, Template, invoke


@pytest.fixture
def client():
    return TestClient(invoke)

def test_invoke_exception_handling(client):
    template = Template('mock_template')
    context = Context('mock_context')

    with patch('src.routes.run.get_node') as mock_get_node:
        mock_get_node.side_effect = Exception('Test exception')

        response = client.post("/invoke/mock_path", json={"template": template, "context": context})

        assert response.status_code == 500
        assert response.json() == 'Test exception'
