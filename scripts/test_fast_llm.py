#!/usr/bin/env python
"""Test Fast LLM implementation with hybrid strategy."""

import os
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.configs.settings import get_settings
from repomind.generation.llm_service import LLMService
from repomind.indexing.embedding_service import EmbeddingService
from repomind.storage.faiss_store import FAISSStore

from repomind.baselines.full_system_fast import FullSystemFast


def main():
    settings = get_settings()
    test_repo_path = Path(__file__).parent.parent / "测试仓库"
    results_dir = Path(__file__).parent.parent / "baseline_results"
    results_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("RepoMind Fast LLM 测试")
    print("=" * 80)
    print(f"Test repository: {test_repo_path}")
    print()

    print("[1/4] Initializing services...")

    # Strong LLM (qwen3.5-plus)
    llm_service_strong = LLMService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model
    )

    # Fast LLM (qwen-flash)
    llm_service_fast = LLMService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model_fast
    )

    embedding_service = EmbeddingService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.embedding_model
    )

    test_queries = [
        "这个项目是做什么的？",
        "有哪些可用的工具函数？",
        "OpenAICompatibleClient 类如何使用？",
        "找到所有与天气相关的代码",
        "get_weather 函数是什么？",
        "agent.py 文件里有什么？",
    ]

    print("[2/4] Initializing FullSystemFast...")
    full_store = FAISSStore(embedding_service=embedding_service)

    full_system_fast = FullSystemFast(
        vector_store=full_store,
        embedding_service=embedding_service,
        llm_service_strong=llm_service_strong,
        llm_service_fast=llm_service_fast,
        settings=settings
    )
    full_system_fast.index_repository(str(test_repo_path))

    print("[3/4] Running queries...")
    print()

    all_results = []

    for query_idx, query in enumerate(test_queries, 1):
        print(f"--- Query {query_idx}: {query}")
        print()

        result = full_system_fast.query(query)
        all_results.append(result)

        print(f"  Query Type: {result.get('query_type', 'unknown')}")
        print(f"  Model Used: {result.get('model_used', 'unknown')}")
        print(f"  Total latency: {result['latency_ms']:.1f}ms")
        print(f"  Tokens: {result['total_tokens']} (prompt: {result['prompt_tokens']}, completion: {result['completion_tokens']})")
        print()

        if "detailed_timings" in result:
            timings = result["detailed_timings"]
            print("  详细耗时:")
            print(f"    - Query Classification:  {timings.get('query_classification', 0):>8.1f} ms")
            print(f"    - Query Expansion:      {timings.get('query_expansion', 0):>8.1f} ms")
            print(f"    - Embedding (3x):        {timings.get('embedding', 0):>8.1f} ms")
            print(f"    - Vector Search:         {timings.get('vector_search', 0):>8.1f} ms")
            print(f"    - Answer Generation:     {timings.get('answer_generation', 0):>8.1f} ms")
            print(f"    {'-' * 40}")
            print(f"    - Total:                {timings.get('total_end_to_end', 0):>8.1f} ms")
        print()

        print("  Answer preview:", result["answer"][:80] if result["answer"] else "(empty)", "...")
        print()
        print("-" * 80)
        print()

    print("[4/4] Generating report...")

    # Calculate summary
    total_latency = sum(r["latency_ms"] for r in all_results)
    avg_latency = total_latency / len(all_results)

    simple_count = sum(1 for r in all_results if r.get("query_type") == "simple")
    complex_count = sum(1 for r in all_results if r.get("query_type") == "complex")

    # Save JSON
    json_path = results_dir / "fast_llm_test_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "queries": test_queries,
            "results": all_results,
            "summary": {
                "total_queries": len(all_results),
                "simple_count": simple_count,
                "complex_count": complex_count,
                "avg_latency_ms": avg_latency,
                "total_latency_ms": total_latency,
            }
        }, f, ensure_ascii=False, indent=2)

    # Save markdown report
    report_path = results_dir / "fast_llm_test_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Fast LLM 测试报告\n\n")
        f.write(f"**测试日期**: 2026-03-23\n\n")
        f.write(f"**测试仓库**: `测试仓库/`\n\n")

        f.write("## 摘要\n\n")
        f.write(f"- **总查询数**: {len(all_results)}\n")
        f.write(f"- **简单问题**: {simple_count}\n")
        f.write(f"- **复杂问题**: {complex_count}\n")
        f.write(f"- **平均延迟**: {avg_latency:.1f} ms\n")
        f.write(f"- **总延迟**: {total_latency:.1f} ms\n\n")

        f.write("## 各查询详情\n\n")
        for query_idx, (query, result) in enumerate(zip(test_queries, all_results), 1):
            f.write(f"### 查询 {query_idx}: {query}\n\n")
            f.write(f"- **问题类型**: {result.get('query_type', 'unknown')}\n")
            f.write(f"- **使用模型**: {result.get('model_used', 'unknown')}\n")
            f.write(f"- **延迟**: {result['latency_ms']:.1f} ms\n")
            f.write(f"- **总 Tokens**: {result['total_tokens']}\n\n")

            if "detailed_timings" in result:
                timings = result["detailed_timings"]
                f.write("**详细耗时**:\n")
                f.write(f"- Query Classification: {timings.get('query_classification', 0):.1f} ms\n")
                f.write(f"- Query Expansion: {timings.get('query_expansion', 0):.1f} ms\n")
                f.write(f"- Answer Generation: {timings.get('answer_generation', 0):.1f} ms\n\n")

            f.write("**答案**:\n")
            f.write(f"{result['answer']}\n\n")
            f.write("---\n\n")

    print(f"  JSON 结果 saved to: {json_path}")
    print(f"  报告 saved to: {report_path}")
    print()
    print("[4/4] Complete!")


if __name__ == "__main__":
    main()
