#!/usr/bin/env python
"""Run baseline comparison tests for RepoMind."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.configs.settings import get_settings
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind.indexing.embedding_service import EmbeddingService
from repomind.storage.faiss_store import FAISSStore
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker
from repomind.retrieval.pipeline import RetrievalPipeline

from repomind.baselines.llm_only import LLMOnly
from repomind.baselines.naive_rag import NaiveRAG
from repomind.baselines.structured_rag import StructuredRAG
from repomind.baselines.full_system import FullSystem
from repomind.baselines.full_system_fast import FullSystemFast


def main():
    settings = get_settings()
    test_repo_path = Path(__file__).parent.parent / "测试仓库"
    results_dir = Path(__file__).parent.parent / "baseline_results"
    results_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("RepoMind Baseline Comparison Test")
    print("=" * 80)
    print(f"Test repository: {test_repo_path}")
    print()

    print("[1/6] Initializing services...")
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

    answer_generator = AnswerGenerator(llm_service=llm_service)

    test_queries = [
        "这个项目是做什么的？",
        "有哪些可用的工具函数？",
        "OpenAICompatibleClient 类如何使用？",
        "找到所有与天气相关的代码",
    ]

    print("[2/6] Initializing systems...")

    print("  - LLM-only")
    llm_only = LLMOnly(llm_service=llm_service)
    llm_only.load_repository(str(test_repo_path))

    print("  - Naive RAG")
    naive_store = FAISSStore(embedding_service=embedding_service)
    naive_rag = NaiveRAG(
        vector_store=naive_store,
        embedding_service=embedding_service,
        answer_generator=answer_generator,
        top_k=5
    )
    naive_rag.index_repository(str(test_repo_path))

    print("  - Structured RAG")
    structured_store = FAISSStore(embedding_service=embedding_service)
    structured_rag = StructuredRAG(
        vector_store=structured_store,
        embedding_service=embedding_service,
        answer_generator=answer_generator,
        top_k=5
    )
    structured_rag.index_repository(str(test_repo_path))

    print("  - Full System")
    full_store = FAISSStore(embedding_service=embedding_service)
    query_expander = QueryExpander(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model
    )
    full_pipeline = RetrievalPipeline(
        vector_store=full_store,
        embedding_service=embedding_service,
        query_expander=query_expander,
        metadata_filter=MetadataFilter(),
        reranker=Reranker(alpha=settings.rerank_alpha, beta=settings.rerank_beta),
        context_packer=ContextPacker(max_tokens=settings.max_context_tokens),
        top_k=settings.retrieval_top_k,
        final_k=settings.retrieval_final_k
    )
    full_system = FullSystem(
        vector_store=full_store,
        embedding_service=embedding_service,
        retrieval_pipeline=full_pipeline,
        answer_generator=answer_generator
    )
    full_system.index_repository(str(test_repo_path))

    print("  - Full System Fast")
    full_system_fast = FullSystemFast()
    full_system_fast.index_repository(str(test_repo_path))

    systems = {
        "LLM-only": llm_only,
        "Naive RAG": naive_rag,
        "Structured RAG": structured_rag,
        "Full System": full_system,
        "Full System Fast": full_system_fast,
    }

    print("[3/6] Running queries...")
    print()

    all_results = {}

    for query_idx, query in enumerate(test_queries, 1):
        print(f"--- Query {query_idx}: {query}")
        print()

        all_results[query] = {}

        for system_name, system in systems.items():
            print(f"  Running {system_name}...")
            result = system.query(query)

            all_results[query][system_name] = result

            print(f"    Latency: {result['latency_ms']:.1f}ms")
            print(f"    Tokens: {result['total_tokens']} (prompt: {result['prompt_tokens']}, completion: {result['completion_tokens']})")
            print(f"    Answer preview: {result['answer'][:100]}...")
            print()

        print("-" * 80)
        print()

    print("[4/6] Saving prompts...")
    prompts_dir = results_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    for query_idx, (query, system_results) in [(i+1, qr) for i, qr in enumerate(all_results.items())]:
        safe_query_name = query.replace("?", "_").replace(" ", "_")[:30]
        for system_name, result in system_results.items():
            safe_system_name = system_name.replace(" ", "_")
            prompt_file = prompts_dir / f"query{query_idx}_{safe_system_name}_{safe_query_name}.md"

            if result.get("full_prompt"):
                with open(prompt_file, "w", encoding="utf-8") as f:
                    f.write(f"# Prompt - {system_name}\n\n")
                    f.write(f"**查询**: {query}\n\n")
                    f.write("---\n\n")
                    f.write("## System Prompt\n\n")
                    f.write(f"```\n{result['full_prompt']['system_prompt']}\n```\n\n")
                    f.write("---\n\n")
                    f.write("## User Prompt\n\n")
                    f.write(f"```\n{result['full_prompt']['user_prompt']}\n```\n")

    print(f"  Prompts saved to: {prompts_dir}/")
    print()

    print("[5/6] Generating report...")
    report_path = results_dir / "comparison_report.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# RepoMind 基线对比测试报告\n\n")
        f.write(f"**测试日期**: 2026-03-23\n\n")
        f.write(f"**测试仓库**: `测试仓库/`\n\n")

        f.write("## 系统说明\n\n")
        f.write("| 系统 | 特点 |\n")
        f.write("|------|------|\n")
        f.write("| LLM-only | 无检索 |\n")
        f.write("| Naive RAG | 文件级 chunk |\n")
        f.write("| Structured RAG | 函数级 chunk（但无 MQE/rerank） |\n")
        f.write("| Full System | 完整优化（qwen3.5-plus） |\n")
        f.write("| Full System Fast | 完整优化 + 双模型策略（qwen-flash + qwen3.5-plus） |\n\n")

        f.write("## 对比结果汇总\n\n")

        for query_idx, (query, system_results) in [(i+1, qr) for i, qr in enumerate(all_results.items())]:
            f.write(f"### 查询 {query_idx}: {query}\n\n")
            f.write("| 系统 | Latency (ms) | Prompt Tokens | Completion Tokens | Total Tokens |\n")
            f.write("|------|--------------|---------------|--------------------|--------------|\n")

            for system_name, result in system_results.items():
                f.write(f"| {system_name} | {result['latency_ms']:.1f} | {result['prompt_tokens']} | {result['completion_tokens']} | {result['total_tokens']} |\n")
            f.write("\n")

            f.write("#### 详细答案\n\n")
            for system_name, result in system_results.items():
                f.write(f"**{system_name}**:\n\n")
                f.write(f"{result['answer']}\n\n")
                if result['sources']:
                    f.write("**源文件**:\n")
                    for source in result['sources']:
                        f.write(f"- {source}\n")
                    f.write("\n")
                f.write("---\n\n")

        f.write("\n## 总结\n\n")
        f.write("此报告为基线对比测试结果，留档保存。\n")
        f.write("\n**注**: 完整的 prompt 已单独保存在 `prompts/` 目录下。\n")

    print(f"  Report saved to: {report_path}")
    print()
    print("[6/6] Complete!")


if __name__ == "__main__":
    main()
