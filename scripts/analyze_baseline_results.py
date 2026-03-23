#!/usr/bin/env python
"""Analyze baseline test results and calculate metrics."""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.evaluation.retrieval_metrics import RetrievalMetrics


def load_expected_sources(test_suite_dir: Path, repo: str) -> Dict[str, List[str]]:
    """Load expected sources from test suite."""
    expected_file = test_suite_dir / repo / "expected_sources.json"
    if not expected_file.exists():
        return {}

    with open(expected_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    question_sources = {}
    for qid, qdata in data.get("question_sources", {}).items():
        question_sources[qid] = qdata.get("files", [])

    return question_sources


def extract_sources_from_report(report_path: Path) -> Dict[int, List[str]]:
    """Extract retrieved sources from comparison report."""
    if not report_path.exists():
        return {}

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    query_sources = {}
    current_query_id = None
    in_sources_section = False

    lines = content.split("\n")
    for line in lines:
        # Match query header with ID
        query_match = re.match(r"### 查询 \d+ \(ID: (\d+),", line)
        if query_match:
            current_query_id = int(query_match.group(1))
            in_sources_section = False
            continue

        # Match sources section
        if "**源文件**:" in line:
            in_sources_section = True
            if current_query_id is not None and current_query_id not in query_sources:
                query_sources[current_query_id] = []
            continue

        # Match source file lines
        if in_sources_section and line.strip().startswith("- "):
            source_path = line.strip()[2:].strip()
            # Extract just the filename or relative path
            if "/测试仓库/" in source_path:
                # Extract path after 测试仓库/
                repo_part = source_path.split("/测试仓库/")[-1]
                # Remove leading slash if present
                if repo_part.startswith("/"):
                    repo_part = repo_part[1:]
                query_sources[current_query_id].append(repo_part)
            else:
                # Just use the filename
                filename = Path(source_path).name
                query_sources[current_query_id].append(filename)

        # End of sources section
        if in_sources_section and line.strip() == "---":
            in_sources_section = False

    return query_sources


def normalize_source_path(path: str) -> str:
    """Normalize source path for comparison."""
    # Just use the filename for matching
    return Path(path).name.lower()


def calculate_metrics_for_system(
    system_name: str,
    repo: str,
    report_path: Path,
    expected_sources: Dict[str, List[str]],
) -> Dict[str, Any]:
    """Calculate metrics for a single system."""
    retrieved_sources = extract_sources_from_report(report_path)

    query_metrics = []
    all_retrieved = []
    all_expected = []

    for qid_str, expected in expected_sources.items():
        qid = int(qid_str)
        retrieved = retrieved_sources.get(qid, [])

        # Normalize paths for comparison
        expected_normalized = [normalize_source_path(p) for p in expected]
        retrieved_normalized = [normalize_source_path(p) for p in retrieved]

        # Calculate metrics
        expected_set = set(expected_normalized)
        metrics = RetrievalMetrics.evaluate_single_query(
            retrieved_normalized,
            expected_normalized
        )

        query_metrics.append({
            "query_id": qid,
            "expected": expected,
            "retrieved": retrieved,
            "metrics": metrics
        })

        all_retrieved.extend(retrieved_normalized)
        all_expected.extend(expected_normalized)

    # Aggregate metrics
    aggregated = RetrievalMetrics.aggregate_query_metrics(
        [m["metrics"] for m in query_metrics]
    )

    return {
        "system": system_name,
        "repo": repo,
        "query_metrics": query_metrics,
        "aggregated": aggregated,
        "total_expected": len(all_expected),
        "total_retrieved": len(all_retrieved)
    }


def main():
    """Main analysis function."""
    repo_root = Path(__file__).parent.parent
    test_suite_dir = repo_root / "test_suite"
    results_archive = repo_root / "baseline_results_archive"

    # Load expected sources
    travel_expected = load_expected_sources(test_suite_dir, "travel_agent")
    cuezero_expected = load_expected_sources(test_suite_dir, "cuezero")

    all_results = []

    # Analyze travel_agent results
    travel_systems = [
        ("llm_only", "travel_agent"),
        ("naive_rag", "travel_agent"),
        ("structured_rag", "travel_agent"),
        ("full_system", "travel_agent"),
        ("full_system_fast", "travel_agent"),
    ]

    for sys_name, repo in travel_systems:
        report_path = results_archive / f"baseline_results_{repo}_{sys_name}" / "comparison_report.md"
        if report_path.exists():
            print(f"Analyzing {repo} - {sys_name}...")
            results = calculate_metrics_for_system(
                sys_name, repo, report_path, travel_expected
            )
            all_results.append(results)

    # Analyze cuezero results
    cuezero_systems = [
        ("llm_only", "cuezero"),
        ("naive_rag", "cuezero"),
        ("structured_rag", "cuezero"),
        ("full_system", "cuezero"),
        ("full_system_fast", "cuezero"),
    ]

    for sys_name, repo in cuezero_systems:
        report_path = results_archive / f"baseline_results_{repo}_{sys_name}" / "comparison_report.md"
        if report_path.exists():
            print(f"Analyzing {repo} - {sys_name}...")
            results = calculate_metrics_for_system(
                sys_name, repo, report_path, cuezero_expected
            )
            all_results.append(results)

    # Generate summary report
    output_path = repo_root / "baseline_metrics_summary.md"
    generate_summary_report(all_results, output_path)

    print(f"\nAnalysis complete! Summary saved to: {output_path}")


def generate_summary_report(all_results: List[Dict[str, Any]], output_path: Path):
    """Generate a comprehensive summary report."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# RepoMind 基线测试指标总结\n\n")
        f.write(f"**测试日期**: 2026-03-23\n\n")

        # Summary by repo
        for repo in ["travel_agent", "cuezero"]:
            f.write(f"## {repo} 项目\n\n")

            repo_results = [r for r in all_results if r["repo"] == repo]

            # Metrics table
            f.write("| 系统 | 平均召回率 | 平均命中率 | 平均精确率 |\n")
            f.write("|------|-----------|-----------|-----------|\n")

            for result in repo_results:
                agg = result["aggregated"]
                f.write(f"| {result['system']} | {agg.get('avg_recall', 0):.3f} | {agg.get('avg_hit_rate', 0):.3f} | {agg.get('avg_precision', 0):.3f} |\n")

            f.write("\n")

            # Detailed per-query metrics
            f.write("### 详细查询指标\n\n")
            for result in repo_results:
                f.write(f"#### {result['system']}\n\n")
                f.write("| 查询ID | 召回率 | 命中率 | 精确率 | 期望文件数 | 检索文件数 |\n")
                f.write("|--------|--------|--------|--------|-----------|-----------|\n")

                for qm in result["query_metrics"]:
                    m = qm["metrics"]
                    f.write(f"| {qm['query_id']} | {m['recall']:.3f} | {m['hit_rate']:.3f} | {m['precision']:.3f} | {len(qm['expected'])} | {len(qm['retrieved'])} |\n")

                f.write("\n")

        # Overall comparison
        f.write("## 总体对比\n\n")
        f.write("| 项目 | 系统 | 平均召回率 | 平均命中率 | 平均精确率 |\n")
        f.write("|------|------|-----------|-----------|-----------|\n")

        for result in all_results:
            agg = result["aggregated"]
            f.write(f"| {result['repo']} | {result['system']} | {agg.get('avg_recall', 0):.3f} | {agg.get('avg_hit_rate', 0):.3f} | {agg.get('avg_precision', 0):.3f} |\n")

        f.write("\n## 指标说明\n\n")
        f.write("- **召回率 (Recall)**: 检索到的相关文件数 / 总相关文件数\n")
        f.write("- **命中率 (Hit Rate)**: 是否至少检索到一个相关文件 (1.0 或 0.0)\n")
        f.write("- **精确率 (Precision)**: 检索到的相关文件数 / 总检索文件数\n")


if __name__ == "__main__":
    main()
