import tempfile
import os
import pytest
from repomind.ingestion.models import CodeChunk
from repomind.storage.faiss_store import FAISSStore


def test_faiss_store_basic():
    """Test basic FAISS store functionality."""
    store = FAISSStore()

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

    embedding1 = [0.1] * 128
    embedding2 = [0.2] * 128

    store.add([chunk1, chunk2], [embedding1, embedding2])

    results = store.search([0.11] * 128, top_k=2)
    assert len(results) == 2


def test_faiss_store_save_load():
    """Test saving and loading FAISS store."""
    store = FAISSStore()

    chunk = CodeChunk(
        content="def test(): return 42",
        file_path="/test.py",
        function_name="test",
        language="python"
    )
    store.add([chunk], [[0.1] * 128])

    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "test_index")
        store.save(path)

        loaded = FAISSStore.load(path)
        assert len(loaded.chunks) == 1
        assert loaded.chunks[0].function_name == "test"
