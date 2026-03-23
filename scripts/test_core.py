#!/usr/bin/env python
"""Test the unified RepoMind core interface."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind import RepoMind


def main():
    print("=" * 80)
    print("RepoMind Core 测试")
    print("=" * 80)
    print()

    test_repo_path = Path(__file__).parent.parent / "测试仓库"

    print("[1/3] 初始化 RepoMind...")
    repomind = RepoMind(
        enable_query_expansion=True,
        enable_query_classification=True,
        query_expansion_variants=2,
        use_fast_llm_for_expansion=True,
        use_hybrid_answer_generation=True,
    )
    print("  初始化完成")
    print()

    print("[2/3] 索引仓库...")
    result = repomind.index_repository(str(test_repo_path))
    print(f"  索引成功: {result['success']}")
    print(f"  Chunk 数量: {result['num_chunks']}")
    print(f"  耗时: {result['latency_ms']:.1f}ms")
    print()

    test_queries = [
        "这个项目是做什么的？",
        "有哪些可用的工具函数？",
        "get_weather 函数是什么？",
        "找到所有与天气相关的代码",
    ]

    print("[3/3] 测试查询...")
    print()

    for query_idx, query in enumerate(test_queries, 1):
        print(f"--- 查询 {query_idx}: {query}")
        print()

        result = repomind.query(query)

        print(f"  问题类型: {result.get('query_type', 'N/A')}")
        print(f"  使用模型: {result.get('model_used', 'N/A')}")
        print(f"  总延迟: {result['latency_ms']:.1f}ms")
        print(f"  Tokens: {result['total_tokens']} (prompt: {result['prompt_tokens']}, completion: {result['completion_tokens']})")
        print()

        if "detailed_timings" in result:
            timings = result["detailed_timings"]
            print("  详细耗时:")
            if "query_classification" in timings:
                print(f"    - Query Classification:  {timings['query_classification']:>8.1f} ms")
            if "query_expansion" in timings:
                print(f"    - Query Expansion:       {timings['query_expansion']:>8.1f} ms")
            print(f"    - Answer Generation:     {timings.get('answer_generation', 0):>8.1f} ms")
            print(f"    {'-' * 40}")
            print(f"    - Total:                 {timings.get('total_end_to_end', 0):>8.1f} ms")
        print()

        print("  答案预览:", result["answer"][:100] if result["answer"] else "(empty)", "...")
        print()
        print("-" * 80)
        print()

    print("[3/3] 完成!")


if __name__ == "__main__":
    main()
