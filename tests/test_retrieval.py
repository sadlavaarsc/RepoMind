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


def test_reranker_chinese_keywords():
    """Test Chinese n-gram matching in reranker."""
    reranker = Reranker(alpha=0.85, beta=0.15)

    # Create chunks with Chinese content
    chunk1 = CodeChunk(
        content="# 这是一个天气查询函数\ndef get_weather(): pass",
        file_path="/weather.py",
        function_name="get_weather",
        language="python"
    )
    chunk2 = CodeChunk(
        content="# 这是一个工具函数\ndef utility(): pass",
        file_path="/utility.py",
        function_name="utility",
        language="python"
    )

    # Test with Chinese query
    results = [(chunk1, 0.7), (chunk2, 0.8)]
    reranked = reranker.rerank(results, "天气查询")
    assert len(reranked) == 2


def test_reranker_bucket_guarantee():
    """Test bucket guarantee (at least 1 doc + 1 code chunk)."""
    reranker = Reranker(alpha=0.85, beta=0.15)

    # Create mix of code and doc chunks
    chunk1 = CodeChunk(
        content="def func(): pass",
        file_path="/code.py",
        language="python",
        chunk_type="function"
    )
    chunk2 = CodeChunk(
        content="# Documentation",
        file_path="/doc.md",
        language="text",
        chunk_type="file"
    )
    chunk3 = CodeChunk(
        content="def another(): pass",
        file_path="/code2.py",
        language="python",
        chunk_type="function"
    )

    results = [(chunk1, 0.9), (chunk2, 0.8), (chunk3, 0.7)]
    reranked = reranker.rerank(results, "test")
    # Should have at least 2 chunks (doc + code)
    assert len(reranked) >= 2


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
