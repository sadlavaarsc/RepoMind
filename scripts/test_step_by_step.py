#!/usr/bin/env python
"""Step-by-step test script to debug RepoMind."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_step_1_settings():
    """Test loading settings."""
    print("\n[Step 1] Testing settings...")
    try:
        from repomind.configs.settings import get_settings
        settings = get_settings()
        print(f"  ✓ Settings loaded")
        print(f"  - API key: {settings.qwen_api_key[:10]}...")
        print(f"  - Base URL: {settings.base_url}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_step_2_ingestion():
    """Test ingestion module."""
    print("\n[Step 2] Testing ingestion...")
    try:
        from repomind.ingestion.chunker import Chunker
        test_repo = Path(__file__).parent.parent / "测试仓库"
        chunker = Chunker()
        chunks = chunker.chunk_repository(str(test_repo))
        print(f"  ✓ Ingestion complete")
        print(f"  - Found {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:3]):
            print(f"  - Chunk {i+1}: {chunk.file_path} {'::' + chunk.function_name if chunk.function_name else ''}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_step_3_embedding():
    """Test embedding service."""
    print("\n[Step 3] Testing embedding service...")
    try:
        from repomind.configs.settings import get_settings
        from repomind.indexing.embedding_service import EmbeddingService

        settings = get_settings()
        service = EmbeddingService(
            api_key=settings.qwen_api_key,
            base_url=settings.base_url,
            model=settings.embedding_model
        )
        embedding = service.embed("def test(): pass")
        print(f"  ✓ Embedding service working")
        print(f"  - Embedding dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_step_4_llm():
    """Test LLM service."""
    print("\n[Step 4] Testing LLM service...")
    try:
        from repomind.configs.settings import get_settings
        from repomind.generation.llm_service import LLMService

        settings = get_settings()
        service = LLMService(
            api_key=settings.qwen_api_key,
            base_url=settings.base_url,
            model=settings.llm_model
        )
        result = service.generate("Hello, please reply with just 'OK'")
        print(f"  ✓ LLM service working")
        print(f"  - Response: {result['content'][:50]}...")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("RepoMind Step-by-Step Debug Test")
    print("=" * 60)

    results = []
    results.append(("Settings", test_step_1_settings()))
    results.append(("Ingestion", test_step_2_ingestion()))
    results.append(("Embedding", test_step_3_embedding()))
    results.append(("LLM", test_step_4_llm()))

    print("\n" + "=" * 60)
    print("Summary:")
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
