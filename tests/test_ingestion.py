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


def test_python_parser():
    """Test Python AST parser."""
    parser = PythonParser()

    test_code = """
def hello():
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
