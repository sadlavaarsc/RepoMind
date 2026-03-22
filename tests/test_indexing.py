import pytest
from repomind.indexing.embedding_service import EmbeddingService


def test_embedding_service_init():
    """Test EmbeddingService initialization."""
    service = EmbeddingService(
        api_key="test_key",
        base_url="https://test.url",
        model="test-model"
    )
    assert service.api_key == "test_key"
    assert service.base_url == "https://test.url"
    assert service.model == "test-model"
