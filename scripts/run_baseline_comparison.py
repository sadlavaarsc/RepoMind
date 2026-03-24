#!/usr/bin/env python
"""Run baseline comparison tests for RepoMind."""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

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


# Available systems for testing
ALL_SYSTEMS = {
    "llm_only": "LLM-only",
    "naive_rag": "Naive RAG",
    "structured_rag": "Structured RAG",
    "full_system": "Full System",
    "full_system_fast": "Full System Fast",
}

# Legacy hardcoded queries (fallback)
LEGACY_QUERIES = [
    "这个项目是做什么的？",
    "有哪些可用的工具函数？",
    "OpenAICompatibleClient 类如何使用？",
    "找到所有与天气相关的代码",
]


def get_system_key(display_name: str) -> str:
    """Get system key from display name."""
    for key, name in ALL_SYSTEMS.items():
        if name == display_name:
            return key
    return display_name.lower().replace(" ", "_")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run baseline comparison tests for RepoMind"
    )

    # System selection
    parser.add_argument(
        "--include",
        type=str,
        default=None,
        help="Comma-separated list of systems to include (e.g., full_system_fast,naive_rag)"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default=None,
        help="Comma-separated list of systems to exclude"
    )

    # Cache options
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="./data/index_cache",
        help="Directory to store index cache (default: ./data/index_cache)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable cache, force reindexing"
    )

    # Test repo path (for indexing)
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Path to test repository (default: depends on --test-repo)"
    )

    # Test suite options
    parser.add_argument(
        "--test-suite",
        type=str,
        default="./test_suite",
        help="Path to test suite directory (default: ./test_suite)"
    )
    parser.add_argument(
        "--test-repo",
        type=str,
        default=None,
        choices=["travel_agent", "cuezero"],
        help="Test repository to use (travel_agent or cuezero)"
    )
    parser.add_argument(
        "--suffix",
        type=str,
        default=None,
        help="Suffix to append to results directory (e.g., 'new_chunk')"
    )
    parser.add_argument(
        "--queries",
        type=str,
        default=None,
        help="Comma-separated list of query numbers to test (e.g., 1,2,3)"
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        default=None,
        help="Comma-separated list of difficulties to test (simple,medium,complex)"
    )

    return parser.parse_args()


def load_test_suite(test_suite_dir: Path, test_repo: str) -> List[Dict[str, Any]]:
    """Load test questions from test suite."""
    test_file = test_suite_dir / test_repo / "test_questions.json"

    if not test_file.exists():
        print(f"Warning: Test file not found: {test_file}")
        print("Falling back to legacy queries")
        return [{"id": i + 1, "question": q, "difficulty": "unknown"}
                for i, q in enumerate(LEGACY_QUERIES)]

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("questions", [])


def filter_queries(queries: List[Dict[str, Any]], args) -> List[Dict[str, Any]]:
    """Filter queries based on arguments."""
    filtered = queries

    # Filter by query numbers
    if args.queries:
        query_nums = set(int(n.strip()) for n in args.queries.split(","))
        filtered = [q for q in filtered if q.get("id") in query_nums]

    # Filter by difficulty
    if args.difficulty:
        difficulties = set(d.strip().lower() for d in args.difficulty.split(","))
        filtered = [q for q in filtered if q.get("difficulty", "unknown").lower() in difficulties]

    return filtered


def get_default_repo_path(test_repo: str) -> Path:
    """Get default repo path based on test_repo."""
    base_path = Path(__file__).parent.parent / "测试仓库"
    if test_repo == "travel_agent":
        return base_path / "旅行agent"
    elif test_repo == "cuezero":
        return base_path / "CueZero"
    return base_path


def get_selected_systems(args) -> dict:
    """Get selected systems based on args."""
    if args.include and args.exclude:
        print("Error: Cannot specify both --include and --exclude")
        sys.exit(1)

    if args.include:
        included = [s.strip() for s in args.include.split(",")]
        selected = {}
        for sys_key in included:
            if sys_key in ALL_SYSTEMS:
                selected[sys_key] = ALL_SYSTEMS[sys_key]
            else:
                print(f"Warning: Unknown system '{sys_key}', skipping")
        if not selected:
            print("Error: No valid systems specified in --include")
            sys.exit(1)
        return selected

    if args.exclude:
        excluded = [s.strip() for s in args.exclude.split(",")]
        selected = {}
        for sys_key, sys_name in ALL_SYSTEMS.items():
            if sys_key not in excluded:
                selected[sys_key] = sys_name
        return selected

    # Default: all systems
    return ALL_SYSTEMS.copy()


def get_cache_path(cache_dir: Path, repo_name: str, system_key: str) -> Path:
    """Get cache file path for a system."""
    safe_repo_name = repo_name.replace("/", "_").replace(" ", "_")
    return cache_dir / f"{safe_repo_name}_{system_key}"


def main():
    args = parse_args()
    settings = get_settings()

    # Get test repo path for indexing
    if args.repo:
        test_repo_path = Path(args.repo)
    elif args.test_repo:
        test_repo_path = get_default_repo_path(args.test_repo)
    else:
        test_repo_path = Path(__file__).parent.parent / "测试仓库"

    repo_name = test_repo_path.name

    # Load test queries
    if args.test_repo:
        print(f"[0/6] Loading test suite: {args.test_repo}")
        test_suite_dir = Path(args.test_suite)
        all_test_queries = load_test_suite(test_suite_dir, args.test_repo)
        test_queries_data = filter_queries(all_test_queries, args)
        test_queries = [q["question"] for q in test_queries_data]
        print(f"  Loaded {len(test_queries)} queries")
    else:
        print("[0/6] Using legacy queries")
        test_queries_data = [{"id": i + 1, "question": q, "difficulty": "unknown"}
                              for i, q in enumerate(LEGACY_QUERIES)]
        test_queries = LEGACY_QUERIES

    results_dir_name = "baseline_results"
    if args.suffix:
        results_dir_name += f"_{args.suffix}"
    results_dir = Path(__file__).parent.parent / results_dir_name
    results_dir.mkdir(exist_ok=True, parents=True)

    # Setup cache directory
    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    use_cache = not args.no_cache

    # Get selected systems
    selected_systems = get_selected_systems(args)
    selected_display_names = list(selected_systems.values())

    print("=" * 80)
    print("RepoMind Baseline Comparison Test")
    print("=" * 80)
    print(f"Test repository: {test_repo_path}")
    if args.test_repo:
        print(f"Test suite: {args.test_repo} ({len(test_queries)} queries)")
        if args.queries:
            print(f"Query selection: #{args.queries}")
        if args.difficulty:
            print(f"Difficulty filter: {args.difficulty}")
    print(f"Selected systems: {', '.join(selected_display_names)}")
    if use_cache:
        print(f"Cache directory: {cache_dir}")
    else:
        print("Cache: disabled (forced reindexing)")
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

    print("[2/6] Initializing systems...")
    systems = {}

    # Initialize LLM-only (no vector store needed)
    if "llm_only" in selected_systems:
        print(f"  - {ALL_SYSTEMS['llm_only']}")
        llm_only = LLMOnly(llm_service=llm_service)
        llm_only.load_repository(str(test_repo_path))
        systems[ALL_SYSTEMS["llm_only"]] = llm_only

    # Initialize Naive RAG
    if "naive_rag" in selected_systems:
        print(f"  - {ALL_SYSTEMS['naive_rag']}")
        cache_path = get_cache_path(cache_dir, repo_name, "naive_rag")

        if use_cache and (cache_path.with_suffix(".index").exists() or cache_path.with_suffix(".pkl").exists()):
            print(f"    Loading from cache: {cache_path}")
            naive_store = FAISSStore.load(str(cache_path), embedding_service=embedding_service)
            naive_rag = NaiveRAG(
                vector_store=naive_store,
                embedding_service=embedding_service,
                answer_generator=answer_generator,
                top_k=5
            )
        else:
            naive_store = FAISSStore(embedding_service=embedding_service)
            naive_rag = NaiveRAG(
                vector_store=naive_store,
                embedding_service=embedding_service,
                answer_generator=answer_generator,
                top_k=5
            )
            naive_rag.index_repository(str(test_repo_path))
            if use_cache:
                print(f"    Saving to cache: {cache_path}")
                naive_store.save(str(cache_path))

        systems[ALL_SYSTEMS["naive_rag"]] = naive_rag

    # Initialize Structured RAG
    if "structured_rag" in selected_systems:
        print(f"  - {ALL_SYSTEMS['structured_rag']}")
        cache_path = get_cache_path(cache_dir, repo_name, "structured_rag")

        if use_cache and (cache_path.with_suffix(".index").exists() or cache_path.with_suffix(".pkl").exists()):
            print(f"    Loading from cache: {cache_path}")
            structured_store = FAISSStore.load(str(cache_path), embedding_service=embedding_service)
            structured_rag = StructuredRAG(
                vector_store=structured_store,
                embedding_service=embedding_service,
                answer_generator=answer_generator,
                top_k=5
            )
        else:
            structured_store = FAISSStore(embedding_service=embedding_service)
            structured_rag = StructuredRAG(
                vector_store=structured_store,
                embedding_service=embedding_service,
                answer_generator=answer_generator,
                top_k=5
            )
            structured_rag.index_repository(str(test_repo_path))
            if use_cache:
                print(f"    Saving to cache: {cache_path}")
                structured_store.save(str(cache_path))

        systems[ALL_SYSTEMS["structured_rag"]] = structured_rag

    # Initialize Full System
    if "full_system" in selected_systems:
        print(f"  - {ALL_SYSTEMS['full_system']}")
        cache_path = get_cache_path(cache_dir, repo_name, "full_system")

        if use_cache and (cache_path.with_suffix(".index").exists() or cache_path.with_suffix(".pkl").exists()):
            print(f"    Loading from cache: {cache_path}")
            full_store = FAISSStore.load(str(cache_path), embedding_service=embedding_service)
        else:
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

        if not (use_cache and (cache_path.with_suffix(".index").exists() or cache_path.with_suffix(".pkl").exists())):
            full_system.index_repository(str(test_repo_path))
            if use_cache:
                print(f"    Saving to cache: {cache_path}")
                full_store.save(str(cache_path))

        systems[ALL_SYSTEMS["full_system"]] = full_system

    # Initialize Full System Fast (uses RepoMind core, handles its own caching)
    if "full_system_fast" in selected_systems:
        print(f"  - {ALL_SYSTEMS['full_system_fast']}")
        full_system_fast = FullSystemFast()
        full_system_fast.index_repository(str(test_repo_path))
        systems[ALL_SYSTEMS["full_system_fast"]] = full_system_fast

    print("[3/6] Running queries...")
    print()

    all_results = {}

    for query_idx, query_data in enumerate(test_queries_data, 1):
        query = query_data["question"]
        query_id = query_data.get("id", query_idx)
        difficulty = query_data.get("difficulty", "unknown")
        print(f"--- Query {query_idx} (ID: {query_id}, {difficulty}): {query}")
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
    results_dir.mkdir(exist_ok=True, parents=True)
    prompts_dir.mkdir(exist_ok=True, parents=True)

    for query_idx, query_data in enumerate(test_queries_data, 1):
        query = query_data["question"]
        query_id = query_data.get("id", query_idx)
        system_results = all_results[query]
        safe_query_name = query.replace("?", "_").replace(" ", "_")[:30]
        for system_name, result in system_results.items():
            safe_system_name = system_name.replace(" ", "_")
            prompt_file = prompts_dir / f"query{query_idx}_id{query_id}_{safe_system_name}_{safe_query_name}.md"

            if result.get("full_prompt"):
                with open(prompt_file, "w", encoding="utf-8") as f:
                    f.write(f"# Prompt - {system_name}\n\n")
                    f.write(f"**查询 ID**: {query_id}\n\n")
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
        f.write(f"**测试仓库**: `{repo_name}/`\n\n")
        if args.test_repo:
            f.write(f"**测试集**: {args.test_repo}\n\n")

        f.write("## 系统说明\n\n")
        f.write("| 系统 | 特点 |\n")
        f.write("|------|------|\n")
        for sys_key in selected_systems:
            if sys_key == "llm_only":
                f.write("| LLM-only | 无检索 |\n")
            elif sys_key == "naive_rag":
                f.write("| Naive RAG | 文件级 chunk |\n")
            elif sys_key == "structured_rag":
                f.write("| Structured RAG | 函数级 chunk（但无 MQE/rerank） |\n")
            elif sys_key == "full_system":
                f.write("| Full System | 完整优化（qwen3.5-plus） |\n")
            elif sys_key == "full_system_fast":
                f.write("| Full System Fast | 完整优化 + 双模型策略（qwen-flash + qwen3.5-plus） |\n")
        f.write("\n")

        f.write("## 对比结果汇总\n\n")

        # Iterate through test_queries_data to preserve ID and difficulty info
        for query_idx, query_data in enumerate(test_queries_data, 1):
            query = query_data["question"]
            query_id = query_data.get("id", query_idx)
            difficulty = query_data.get("difficulty", "unknown")
            system_results = all_results[query]

            f.write(f"### 查询 {query_idx} (ID: {query_id}, {difficulty})\n\n")
            f.write(f"**问题**: {query}\n\n")
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
        f.write(f"\n**测试配置**: 测试系统={', '.join(selected_display_names)}\n")
        if args.test_repo:
            f.write(f" 测试集={args.test_repo}\n")
            if args.queries:
                f.write(f" 查询选择=#{args.queries}\n")
            if args.difficulty:
                f.write(f" 难度筛选={args.difficulty}\n")
        f.write("\n**注**: 完整的 prompt 已单独保存在 `prompts/` 目录下。\n")

    print(f"  Report saved to: {report_path}")
    print()
    print("[6/6] Complete!")


if __name__ == "__main__":
    main()
