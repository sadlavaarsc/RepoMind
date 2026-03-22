#!/usr/bin/env python
"""Demo test script - simple repository explanation task."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.configs.settings import get_settings
from repomind.ingestion.chunker import Chunker
from repomind.indexing.embedding_service import EmbeddingService
from repomind.indexing.index_builder import IndexBuilder
from repomind.storage.faiss_store import FAISSStore
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker
from repomind.retrieval.pipeline import RetrievalPipeline
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator


def main():
    settings = get_settings()

    test_repo_path = Path(__file__).parent.parent / "测试仓库"
    print(f"=" * 60)
    print(f"RepoMind Demo Test")
    print(f"=" * 60)
    print(f"Test repository: {test_repo_path}")
    print()

    print("[1/5] Initializing services...")
    embedding_service = EmbeddingService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.embedding_model
    )

    llm_service = LLMService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model
    )

    chunker = Chunker()
    vector_store = FAISSStore(embedding_service=embedding_service)
    index_builder = IndexBuilder(chunker, vector_store, embedding_service)

    print("[2/5] Indexing test repository...")
    index_builder.build_index(str(test_repo_path))
    print(f"   Indexed {len(vector_store.chunks)} chunks")

    print("[3/5] Setting up retrieval pipeline...")
    query_expander = QueryExpander(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model
    )

    retrieval_pipeline = RetrievalPipeline(
        vector_store=vector_store,
        embedding_service=embedding_service,
        query_expander=query_expander,
        metadata_filter=MetadataFilter(),
        reranker=Reranker(alpha=settings.rerank_alpha, beta=settings.rerank_beta),
        context_packer=ContextPacker(max_tokens=settings.max_context_tokens),
        top_k=settings.retrieval_top_k,
        final_k=settings.retrieval_final_k
    )

    answer_generator = AnswerGenerator(llm_service=llm_service)

    test_queries = [
        "这个项目是做什么的？",
        "有哪些可用的工具函数？",
        "OpenAICompatibleClient 类如何使用？",
        "找到所有与天气相关的代码",
    ]

    print("[4/5] Running test queries...")
    print()

    for i, query in enumerate(test_queries, 1):
        print(f"--- Query {i}: {query}")
        print()

        chunks = retrieval_pipeline.retrieve(query)
        result = answer_generator.generate(query, chunks)

        print("Answer:")
        print(result["answer"])
        print()

        if result["sources"]:
            print("Sources:")
            for source in result["sources"]:
                print(f"  - {source}")
            print()

        print(f"Latency: {result.get('latency_ms', 0):.1f}ms")
        print(f"Tokens: {result.get('total_tokens', 0)} (prompt: {result.get('prompt_tokens', 0)}, completion: {result.get('completion_tokens', 0)})")
        print()
        print("-" * 60)
        print()

    print("[5/5] Demo complete!")


if __name__ == "__main__":
    main()
