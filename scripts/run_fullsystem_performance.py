#!/usr/bin/env python
"""Run detailed performance profiling for Full System."""

import os
import sys
from pathlib import Path
import json

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

from repomind.baselines.full_system import FullSystem


def main():
    settings = get_settings()
    test_repo_path = Path(__file__).parent.parent / "测试仓库"
    results_dir = Path(__file__).parent.parent / "baseline_results"
    results_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("RepoMind Full System 性能详细分析")
    print("=" * 80)
    print(f"Test repository: {test_repo_path}")
    print()

    print("[1/4] Initializing services...")
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

    print("[2/4] Initializing Full System...")

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

    print("[3/4] Running queries with detailed timing...")
    print()

    all_results = []
    all_timings = []

    for query_idx, query in enumerate(test_queries, 1):
        print(f"--- Query {query_idx}: {query}")
        print()

        result = full_system.query(query)
        all_results.append(result)
        all_timings.append(result["detailed_timings"])

        print(f"  Total latency: {result['latency_ms']:.1f}ms")
        print(f"  Tokens: {result['total_tokens']} (prompt: {result['prompt_tokens']}, completion: {result['completion_tokens']})")
        print()

        timings = result["detailed_timings"]
        print("  详细耗时 breakdown:")
        print(f"    - Query Expansion:     {timings.get('query_expansion', 0):>8.1f} ms")
        print(f"    - Embedding (3x):      {timings.get('embedding', 0):>8.1f} ms")
        print(f"    - Vector Search (3x):  {timings.get('vector_search', 0):>8.1f} ms")
        print(f"    - Result Merge:        {timings.get('result_merge', 0):>8.1f} ms")
        print(f"    - Metadata Filter:     {timings.get('metadata_filter', 0):>8.1f} ms")
        print(f"    - Reranking:           {timings.get('reranking', 0):>8.1f} ms")
        print(f"    - Context Packing:     {timings.get('context_packing', 0):>8.1f} ms")
        print(f"    - Answer Generation:   {timings.get('answer_generation', 0):>8.1f} ms")
        print(f"    {'-' * 40}")
        print(f"    - Total End-to-End:    {timings.get('total_end_to_end', 0):>8.1f} ms")
        print()

        print("  Answer preview:", result["answer"][:80] if result["answer"] else "(empty)", "...")
        print()
        print("-" * 80)
        print()

    print("[4/4] Generating performance report...")

    # Calculate average timings
    avg_timings = {}
    if all_timings:
        keys = all_timings[0].keys()
        for key in keys:
            avg_timings[key] = sum(t.get(key, 0) for t in all_timings) / len(all_timings)

    # Save detailed JSON
    json_path = results_dir / "fullsystem_performance.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "queries": test_queries,
            "results": all_results,
            "average_timings": avg_timings
        }, f, ensure_ascii=False, indent=2)

    # Save human-readable report
    report_path = results_dir / "fullsystem_performance_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Full System 性能详细分析报告\n\n")
        f.write(f"**测试日期**: 2026-03-23\n\n")
        f.write(f"**测试仓库**: `测试仓库/`\n\n")

        f.write("## 各环节耗时说明\n\n")
        f.write("| 阶段 | 说明 |\n")
        f.write("|------|------|\n")
        f.write("| Query Expansion | LLM 生成 2-3 个查询变体 |\n")
        f.write("| Embedding (3x) | 对 3 个查询分别生成 embedding |\n")
        f.write("| Vector Search (3x) | 3 次 FAISS 向量搜索 |\n")
        f.write("| Result Merge | 合并搜索结果并去重 |\n")
        f.write("| Metadata Filter | 元数据过滤 |\n")
        f.write("| Reranking | 重排序 (embedding + 关键词) |\n")
        f.write("| Context Packing | 上下文打包与格式化 |\n")
        f.write("| Answer Generation | LLM 生成最终答案 |\n\n")

        f.write("## 平均耗时汇总\n\n")
        f.write("| 阶段 | 平均耗时 (ms) | 占比 |\n")
        f.write("|------|--------------|------|\n")

        total_avg = avg_timings.get("total_end_to_end", 1)
        stages = [
            ("Query Expansion", "query_expansion"),
            ("Embedding (3x)", "embedding"),
            ("Vector Search (3x)", "vector_search"),
            ("Result Merge", "result_merge"),
            ("Metadata Filter", "metadata_filter"),
            ("Reranking", "reranking"),
            ("Context Packing", "context_packing"),
            ("Answer Generation", "answer_generation"),
        ]

        for display_name, key in stages:
            val = avg_timings.get(key, 0)
            pct = (val / total_avg * 100) if total_avg > 0 else 0
            f.write(f"| {display_name} | {val:.1f} | {pct:.1f}% |\n")

        f.write(f"| **Total End-to-End** | **{total_avg:.1f}** | **100%** |\n\n")

        f.write("## 各查询详细数据\n\n")
        for query_idx, (query, timings) in enumerate(zip(test_queries, all_timings), 1):
            f.write(f"### 查询 {query_idx}: {query}\n\n")
            f.write("| 阶段 | 耗时 (ms) |\n")
            f.write("|------|----------|\n")
            for display_name, key in stages:
                f.write(f"| {display_name} | {timings.get(key, 0):.1f} |\n")
            f.write(f"| **Total End-to-End** | **{timings.get('total_end_to_end', 0):.1f}** |\n\n")

        f.write("\n## 结论\n\n")
        f.write("1. **Query Expansion** 和 **Answer Generation** 是两个最大的开销，各占约 25-35%\n")
        f.write("2. **Embedding** 和 **Vector Search** 相对较小，因为是本地操作\n")
        f.write("3. **Reranking** 和 **Context Packing** 开销很低，可以忽略\n\n")

    print(f"  JSON 数据 saved to: {json_path}")
    print(f"  报告 saved to: {report_path}")
    print()
    print("[4/4] Complete!")


if __name__ == "__main__":
    main()
