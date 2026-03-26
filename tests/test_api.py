"""
FastAPI 服务单元测试
使用 mock 测试 API 端点
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from repomind.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.fixture
def mock_repomind():
    """Create a mock RepoMind instance."""
    mock = MagicMock()
    mock.is_indexed = False
    return mock


def test_index_repository_missing_path(client):
    """Test index endpoint with non-existent path."""
    with patch("repomind.api.main.repomind", MagicMock()):
        response = client.post("/index", json={"repo_path": "/nonexistent/path"})
        assert response.status_code == 400


def test_query_without_index(client):
    """Test query endpoint without an index."""
    mock_repo = MagicMock()
    mock_repo.is_indexed = False

    with patch("repomind.api.main.repomind", mock_repo):
        response = client.post("/query", json={"question": "test?"})
        assert response.status_code == 400
        assert "No index available" in response.json()["detail"]
