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


def test_faiss_store_count():
    """Test count method."""
    store = FAISSStore()
    assert store.count() == 0

    chunk1 = CodeChunk(content="test1", file_path="/t1.py", language="python")
    chunk2 = CodeChunk(content="test2", file_path="/t2.py", language="python")
    store.add([chunk1, chunk2], [[0.1] * 128, [0.2] * 128])

    assert store.count() == 2


def test_faiss_store_exists():
    """Test exists class method."""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, "test_index")

        # Should not exist initially
        assert FAISSStore.exists(path) is False

        # Create and save
        store = FAISSStore()
        chunk = CodeChunk(content="test", file_path="/t.py", language="python")
        store.add([chunk], [[0.1] * 128])
        store.save(path)

        # Should exist now
        assert FAISSStore.exists(path) is True


def test_faiss_store_get_chunks_by_file():
    """Test get_chunks_by_file method."""
    store = FAISSStore()

    chunk1 = CodeChunk(content="def f1(): pass", file_path="/module/a.py", language="python", function_name="f1")
    chunk2 = CodeChunk(content="def f2(): pass", file_path="/module/a.py", language="python", function_name="f2")
    chunk3 = CodeChunk(content="def f3(): pass", file_path="/module/b.py", language="python", function_name="f3")

    store.add([chunk1, chunk2, chunk3], [[0.1] * 128, [0.2] * 128, [0.3] * 128])

    # Get chunks from /module/a.py
    chunks_a = store.get_chunks_by_file("/module/a.py")
    assert len(chunks_a) == 2
    func_names = [c.function_name for c in chunks_a]
    assert "f1" in func_names
    assert "f2" in func_names

    # Get chunks from /module/b.py
    chunks_b = store.get_chunks_by_file("/module/b.py")
    assert len(chunks_b) == 1
    assert chunks_b[0].function_name == "f3"


def test_faiss_store_delete():
    """Test delete method."""
    store = FAISSStore()

    chunk1 = CodeChunk(content="test1", file_path="/t1.py", language="python")
    chunk2 = CodeChunk(content="test2", file_path="/t2.py", language="python")
    chunk3 = CodeChunk(content="test3", file_path="/t3.py", language="python")

    store.add([chunk1, chunk2, chunk3], [[0.1] * 128, [0.2] * 128, [0.3] * 128])
    assert store.count() == 3

    # Delete chunk1 and chunk3
    store.delete([chunk1.file_path, chunk3.file_path])
    assert store.count() == 1
    remaining_files = [c.file_path for c in store.chunks]
    assert "/t2.py" in remaining_files


def test_faiss_store_update():
    """Test update method."""
    store = FAISSStore()

    chunk = CodeChunk(content="old content", file_path="/t.py", language="python")
    store.add([chunk], [[0.1] * 128])
    assert store.count() == 1
    assert store.chunks[0].content == "old content"

    # Update the chunk
    updated_chunk = CodeChunk(content="new content", file_path="/t.py", language="python")
    store.update([updated_chunk], [[0.2] * 128])

    assert store.count() == 1
    assert store.chunks[0].content == "new content"


def test_faiss_store_clear():
    """Test clear method."""
    store = FAISSStore()

    chunk1 = CodeChunk(content="test1", file_path="/t1.py", language="python")
    chunk2 = CodeChunk(content="test2", file_path="/t2.py", language="python")
    store.add([chunk1, chunk2], [[0.1] * 128, [0.2] * 128])
    assert store.count() == 2
    assert store.index is not None

    # Clear everything
    store.clear()
    assert store.count() == 0
    assert store.index is None
