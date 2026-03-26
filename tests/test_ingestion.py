import os
import tempfile
import pytest
from repomind.ingestion.models import CodeChunk
from repomind.ingestion.parsers.python_parser import PythonParser
from repomind.ingestion.chunker import Chunker


def test_code_chunk_model():
    """Test CodeChunk data model."""
    chunk = CodeChunk(
        content="def test(): pass",
        file_path="/test.py",
        function_name="test",
        class_name=None,
        language="python"
    )
    assert chunk.content == "def test(): pass"
    assert chunk.get_identifier() == "/test.py::test"


def test_code_chunk_new_fields():
    """Test CodeChunk new fields for multi-level chunking."""
    chunk = CodeChunk(
        content="def test(): pass",
        file_path="/test.py",
        function_name="test",
        class_name=None,
        language="python",
        chunk_type="function",
        name="test",
        signature="def test():",
        docstring="Test function",
        summary="This is a test function that does nothing.",
        structured_data={
            "imports": [],
            "calls": [],
            "returns": None
        }
    )
    assert chunk.chunk_type == "function"
    assert chunk.name == "test"
    assert chunk.signature == "def test():"
    assert chunk.docstring == "Test function"
    assert chunk.summary is not None
    assert "calls" in chunk.structured_data


def test_code_chunk_get_embedding_text():
    """Test get_embedding_text method with summary and structured data."""
    chunk = CodeChunk(
        content="def test(): return 42",
        file_path="/test.py",
        function_name="test",
        language="python",
        chunk_type="function",
        name="test",
        summary="Returns the answer to life, universe, and everything.",
        structured_data={
            "calls": [],
            "returns": "int"
        }
    )
    embedding_text = chunk.get_embedding_text()
    assert "[TYPE] function" in embedding_text
    assert "Name: test" in embedding_text
    assert "File: /test.py" in embedding_text
    assert "Summary:" in embedding_text
    assert "Returns the answer" in embedding_text
    assert "Code:" in embedding_text
    assert "def test(): return 42" in embedding_text


def test_python_parser():
    """Test Python AST parser."""
    parser = PythonParser()

    test_code = """def hello():
    print("hello")

class TestClass:
    def method(self):
        return 42
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_code)
        temp_path = f.name

    try:
        chunks = parser.parse_file(temp_path)
        assert len(chunks) >= 2

        function_names = [c.function_name for c in chunks if c.function_name]
        assert "hello" in function_names
        assert "method" in function_names
    finally:
        os.unlink(temp_path)


def test_chunker():
    """Test Chunker orchestrator."""
    chunker = Chunker()

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, "w") as f:
            f.write("def test(): pass")

        chunks = chunker.chunk_repository(temp_dir)
        assert len(chunks) >= 1
