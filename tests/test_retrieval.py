import pytest
from repomind.ingestion.models import CodeChunk
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker


def test_metadata_filter():
    """Test metadata filtering."""
    filter = MetadataFilter()

    chunk1 = CodeChunk(
        content="def test(): pass",
        file_path="/test.py",
        function_name="test",
        language="python"
    )
    chunk2 = CodeChunk(
        content="some content",
        file_path="/test.txt",
        language="text"
    )

    results = [(chunk1, 0.9), (chunk2, 0.8)]
    filtered = filter.filter(results, "test")
    assert len(filtered) >= 1


def test_reranker():
    """Test reranking."""
    reranker = Reranker(alpha=0.7, beta=0.3)

    chunk1 = CodeChunk(
        content="def weather(): pass",
        file_path="/weather.py",
        function_name="weather",
        language="python"
    )
    chunk2 = CodeChunk(
        content="def other(): pass",
        file_path="/other.py",
        function_name="other",
        language="python"
    )

    results = [(chunk1, 0.8), (chunk2, 0.9)]
    reranked = reranker.rerank(results, "weather")
    assert len(reranked) == 2


def test_context_packer():
    """Test context packing."""
    packer = ContextPacker(max_tokens=1000)

    chunk1 = CodeChunk(
        content="def test1(): return 1",
        file_path="/test1.py",
        function_name="test1",
        language="python"
    )
    chunk2 = CodeChunk(
        content="def test2(): return 2",
        file_path="/test2.py",
        function_name="test2",
        language="python"
    )
    chunk3 = CodeChunk(
        content="def test1(): return 1",
        file_path="/test1.py",
        function_name="test1",
        language="python"
    )

    results = [(chunk1, 0.9), (chunk2, 0.8), (chunk3, 0.7)]
    packed = packer.pack(results, final_k=5)
    assert len(packed) == 2
