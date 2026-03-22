import pytest
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator


def test_llm_service_init():
    """Test LLMService initialization."""
    service = LLMService(
        api_key="test_key",
        base_url="https://test.url",
        model="test-model"
    )
    assert service.api_key == "test_key"
    assert service.base_url == "https://test.url"
    assert service.model == "test-model"


def test_answer_generator_format_context():
    """Test context formatting in AnswerGenerator."""
    from repomind.ingestion.models import CodeChunk

    llm_service = LLMService(
        api_key="test_key",
        base_url="https://test.url"
    )
    generator = AnswerGenerator(llm_service)

    chunk = CodeChunk(
        content="def test(): pass",
        file_path="/test.py",
        function_name="test",
        class_name="TestClass",
        language="python"
    )

    context = generator._format_context([chunk])
    assert "/test.py" in context
    assert "test" in context
    assert "TestClass" in context
