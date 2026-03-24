#!/usr/bin/env python
"""Analyze baseline test results and calculate metrics."""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.evaluation.retrieval_metrics import RetrievalMetrics


def load_llm_eval_results(llm_eval_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Load all LLM evaluation results."""
    llm_results = {}
    for eval_file in llm_eval_dir.glob("llm_eval_*.json"):
        if eval_file.name == "llm_eval_summary.json":
            continue
        with open(eval_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            key = f"{data['repo']}_{data['system']}"
            llm_results[key] = data
    return llm_results


def load_test_suite(test_suite_dir: Path, repo: str) -> Dict[str, Any]:
    """Load test suite data including questions and expected answers."""
    test_file = test_suite_dir / repo / "test_questions.json"
    if not test_file.exists():
        return {}

    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


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


def extract_performance_from_report(report_path: Path) -> Dict[int, Dict[str, Any]]:
    """Extract latency and token metrics from comparison report."""
    if not report_path.exists():
        return {}

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    query_performance = {}
    current_query_id = None

    lines = content.split("\n")
    for line in lines:
        # Match query header with ID
        query_match = re.match(r"### 查询 \d+ \(ID: (\d+),", line)
        if query_match:
            current_query_id = int(query_match.group(1))
            continue

        # Match performance table
        if current_query_id is not None and "| 系统 | Latency (ms) |" in line:
            # Next line should be the separator, then data line
            continue

        # Match data line
        perf_match = re.match(r"\|.*\| (\d+\.?\d*) \| (\d+) \| (\d+) \| (\d+) \|", line)
        if perf_match and current_query_id is not None:
            query_performance[current_query_id] = {
                "latency_ms": float(perf_match.group(1)),
                "prompt_tokens": int(perf_match.group(2)),
                "completion_tokens": int(perf_match.group(3)),
                "total_tokens": int(perf_match.group(4)),
            }

    return query_performance


def extract_answers_from_report(report_path: Path) -> Dict[int, str]:
    """Extract actual answers from comparison report."""
    if not report_path.exists():
        return {}

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    query_answers = {}
    current_query_id = None
    in_answer_section = False
    current_answer = []

    lines = content.split("\n")
    for line in lines:
        # Match query header with ID
        query_match = re.match(r"### 查询 \d+ \(ID: (\d+),", line)
        if query_match:
            if current_query_id is not None and current_answer:
                query_answers[current_query_id] = "\n".join(current_answer).strip()
            current_query_id = int(query_match.group(1))
            in_answer_section = False
            current_answer = []
            continue

        # Match detailed answer section
        if "#### 详细答案" in line:
            in_answer_section = True
            continue

        # Match system answer header
        if in_answer_section and line.strip().startswith("**") and line.strip().endswith("**:"):
            continue

        # End of answer (next query or separator)
        if in_answer_section and line.strip() == "---":
            if current_query_id is not None and current_answer:
                query_answers[current_query_id] = "\n".join(current_answer).strip()
            in_answer_section = False
            continue

        # Collect answer content
        if in_answer_section and line.strip() and not line.strip().startswith("**源文件**:") and not line.strip().startswith("参考文件："):
            current_answer.append(line)

    # Add the last answer
    if current_query_id is not None and current_answer:
        query_answers[current_query_id] = "\n".join(current_answer).strip()

    return query_answers


def evaluate_answer_quality(actual_answer: str, expected_entities: List[str], reference_answer: str) -> Dict[str, Any]:
    """Evaluate answer quality based on entity coverage and content."""
    if not actual_answer:
        return {"quality_score": 0.0, "entity_coverage": 0.0, "reason": "No answer provided"}

    # Calculate entity coverage
    actual_lower = actual_answer.lower()
    covered_entities = []
    missed_entities = []

    for entity in expected_entities:
        if entity.lower() in actual_lower:
            covered_entities.append(entity)
        else:
            missed_entities.append(entity)

    entity_coverage = len(covered_entities) / len(expected_entities) if expected_entities else 1.0

    # Calculate overall quality score (simple heuristic)
    # 70% entity coverage, 30% answer length (reasonable length)
    length_score = min(1.0, len(actual_answer) / 200)  # Up to 200 chars gets full score
    quality_score = 0.7 * entity_coverage + 0.3 * length_score

    # Determine reason
    if quality_score >= 0.9:
        reason = "Excellent - covers all key entities and provides detailed explanation"
    elif quality_score >= 0.7:
        reason = "Good - covers most key entities"
    elif quality_score >= 0.5:
        reason = "Fair - covers some key entities but missing important details"
    else:
        reason = "Poor - missing most key entities or incomplete answer"

    return {
        "quality_score": quality_score,
        "entity_coverage": entity_coverage,
        "covered_entities": covered_entities,
        "missed_entities": missed_entities,
        "reason": reason
    }


def normalize_source_path(path: str) -> str:
    """Normalize source path for comparison."""
    # Just use the filename for matching
    return Path(path).name.lower()


def calculate_metrics_for_system(
    system_name: str,
    repo: str,
    report_path: Path,
    expected_sources: Dict[str, List[str]],
    test_suite_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Calculate metrics for a single system."""
    retrieved_sources = extract_sources_from_report(report_path)
    performance_metrics = extract_performance_from_report(report_path)
    actual_answers = extract_answers_from_report(report_path)

    # Create question lookup from test suite
    question_lookup = {}
    if test_suite_data:
        for q in test_suite_data.get("questions", []):
            question_lookup[q["id"]] = q

    query_metrics = []
    all_retrieved = []
    all_expected = []

    total_latency = 0.0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_total_tokens = 0
    total_quality_score = 0.0

    for qid_str, expected in expected_sources.items():
        qid = int(qid_str)
        retrieved = retrieved_sources.get(qid, [])
        perf = performance_metrics.get(qid, {})
        actual_answer = actual_answers.get(qid, "")

        # Normalize paths for comparison
        expected_normalized = [normalize_source_path(p) for p in expected]
        retrieved_normalized = [normalize_source_path(p) for p in retrieved]

        # Calculate retrieval metrics
        expected_set = set(expected_normalized)
        metrics = RetrievalMetrics.evaluate_single_query(
            retrieved_normalized,
            expected_normalized
        )

        # Evaluate answer quality
        quality = None
        question_data = question_lookup.get(qid, {})
        if question_data:
            expected_entities = question_data.get("expected_entities", [])
            reference_answer = question_data.get("reference_answer", "")
            quality = evaluate_answer_quality(actual_answer, expected_entities, reference_answer)
            total_quality_score += quality["quality_score"]

        query_metrics.append({
            "query_id": qid,
            "expected": expected,
            "retrieved": retrieved,
            "metrics": metrics,
            "performance": perf,
            "quality": quality,
            "actual_answer": actual_answer,
        })

        all_retrieved.extend(retrieved_normalized)
        all_expected.extend(expected_normalized)

        # Aggregate performance
        total_latency += perf.get("latency_ms", 0)
        total_prompt_tokens += perf.get("prompt_tokens", 0)
        total_completion_tokens += perf.get("completion_tokens", 0)
        total_total_tokens += perf.get("total_tokens", 0)

    # Aggregate metrics
    aggregated = RetrievalMetrics.aggregate_query_metrics(
        [m["metrics"] for m in query_metrics]
    )

    num_queries = len(query_metrics) if query_metrics else 1

    return {
        "system": system_name,
        "repo": repo,
        "query_metrics": query_metrics,
        "aggregated": aggregated,
        "total_expected": len(all_expected),
        "total_retrieved": len(all_retrieved),
        "avg_quality_score": total_quality_score / num_queries if num_queries > 0 else 0,
        "performance": {
            "avg_latency_ms": total_latency / num_queries,
            "total_latency_ms": total_latency,
            "avg_prompt_tokens": total_prompt_tokens / num_queries,
            "total_prompt_tokens": total_prompt_tokens,
            "avg_completion_tokens": total_completion_tokens / num_queries,
            "total_completion_tokens": total_completion_tokens,
            "avg_total_tokens": total_total_tokens / num_queries,
            "total_total_tokens": total_total_tokens,
        }
    }


def main():
    """Main analysis function."""
    repo_root = Path(__file__).parent.parent
    test_suite_dir = repo_root / "test_suite"
    results_archive = repo_root / "baseline_results_archive"
    llm_eval_dir = repo_root / "llm_evaluation_results"

    # Load expected sources and test suites
    travel_expected = load_expected_sources(test_suite_dir, "travel_agent")
    cuezero_expected = load_expected_sources(test_suite_dir, "cuezero")
    travel_test_suite = load_test_suite(test_suite_dir, "travel_agent")
    cuezero_test_suite = load_test_suite(test_suite_dir, "cuezero")

    # Load answer quality ratings (placeholder)
    quality_ratings = load_answer_quality_ratings()

    # Load LLM evaluation results
    llm_eval_results = load_llm_eval_results(llm_eval_dir)
    print(f"Loaded LLM eval results for {len(llm_eval_results)} systems")

    all_results = []

    # Analyze travel_agent results
    travel_systems = [
        ("llm_only", "travel_agent"),
        ("naive_rag", "travel_agent"),
        ("structured_rag", "travel_agent"),
        ("structured_rag_new_chunk", "travel_agent"),
        ("full_system", "travel_agent"),
        ("full_system_fast", "travel_agent"),
        ("full_system_new_chunk", "travel_agent"),
        ("full_system_fast_new_chunk", "travel_agent"),
    ]

    for sys_name, repo in travel_systems:
        report_path = results_archive / f"baseline_results_{repo}_{sys_name}" / "comparison_report.md"
        if report_path.exists():
            print(f"Analyzing {repo} - {sys_name}...")
            results = calculate_metrics_for_system(
                sys_name, repo, report_path, travel_expected, travel_test_suite
            )
            # Add quality ratings
            add_quality_ratings(results, quality_ratings, repo)
            all_results.append(results)

    # Analyze cuezero results
    cuezero_systems = [
        ("llm_only", "cuezero"),
        ("naive_rag", "cuezero"),
        ("structured_rag", "cuezero"),
        ("structured_rag_new_chunk", "cuezero"),
        ("full_system", "cuezero"),
        ("full_system_fast", "cuezero"),
        ("full_system_new_chunk", "cuezero"),
        ("full_system_fast_new_chunk", "cuezero"),
    ]

    for sys_name, repo in cuezero_systems:
        report_path = results_archive / f"baseline_results_{repo}_{sys_name}" / "comparison_report.md"
        if report_path.exists():
            print(f"Analyzing {repo} - {sys_name}...")
            results = calculate_metrics_for_system(
                sys_name, repo, report_path, cuezero_expected, cuezero_test_suite
            )
            # Add quality ratings
            add_quality_ratings(results, quality_ratings, repo)
            all_results.append(results)

    # Generate summary report
    output_path = repo_root / "baseline_metrics_summary.md"
    generate_summary_report(all_results, output_path, llm_eval_results)

    print(f"\nAnalysis complete! Summary saved to: {output_path}")


def load_answer_quality_ratings() -> Dict[str, Dict[int, int]]:
    """Load answer quality ratings from previous summary."""
    # This is a simplified version - in reality we'd parse the previous summary
    # For now, return empty dict
    return {}


def add_quality_ratings(results: Dict[str, Any], ratings: Dict[str, Dict[int, int]], repo: str):
    """Add quality ratings to results."""
    # This would add quality ratings from previous analysis
    # For now, just add placeholder
    pass


def generate_summary_report(all_results: List[Dict[str, Any]], output_path: Path, llm_eval_results: Dict[str, Dict[str, Any]] = None):
    """Generate a comprehensive summary report."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# RepoMind 基线测试完整指标总结\n\n")
        f.write(f"**测试日期**: 2026-03-24\n\n")

        # Summary by repo
        for repo in ["travel_agent", "cuezero"]:
            f.write(f"## {repo} 项目\n\n")

            repo_results = [r for r in all_results if r["repo"] == repo]

            # Metrics table with quality and LLM eval
            f.write("| 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 可回答率 | 端到端成功率 | 平均充分性 | 平均正确性 | 平均事实性 | 检索差距 | 平均延迟(ms) | 平均总Token |\n")
            f.write("|------|-----------|-----------|-----------|------------|---------|------------|---------|---------|---------|--------|------------|-----------|\n")

            for result in repo_results:
                agg = result["aggregated"]
                perf = result["performance"]
                key = f"{repo}_{result['system']}"
                llm_agg = llm_eval_results.get(key, {}).get("aggregated", {}) if llm_eval_results else {}

                f.write(f"| {result['system']} | {agg.get('avg_recall', 0):.3f} | {agg.get('avg_hit_rate', 0):.3f} | {agg.get('avg_precision', 0):.3f} | {result.get('avg_quality_score', 0):.3f} | {llm_agg.get('answerable_rate', 0):.1%} | {llm_agg.get('end_to_end_success_rate', 0):.1%} | {llm_agg.get('avg_sufficiency', 0):.2f} | {llm_agg.get('avg_correctness', 0):.2f} | {llm_agg.get('avg_grounding', 0):.2f} | {llm_agg.get('retrieval_gap', 0):.2f} | {perf.get('avg_latency_ms', 0):.1f} | {perf.get('avg_total_tokens', 0):.0f} |\n")

            f.write("\n")

            # Detailed per-query metrics
            f.write("### 详细查询指标\n\n")
            for result in repo_results:
                f.write(f"#### {result['system']}\n\n")
                f.write("| 查询ID | 召回率 | 命中率 | 精确率 | 答案质量 | 实体覆盖率 | 延迟(ms) | Prompt Token | Completion Token | 总Token | 期望文件数 | 检索文件数 | 质量说明 |\n")
                f.write("|--------|--------|--------|--------|--------|---------|----------|-------------|-----------------|---------|-----------|-----------|--------|\n")

                for qm in result["query_metrics"]:
                    m = qm["metrics"]
                    p = qm["performance"]
                    q = qm.get("quality", {})
                    quality_score = q.get("quality_score", 0)
                    entity_coverage = q.get("entity_coverage", 0)
                    reason = q.get("reason", "")
                    f.write(f"| {qm['query_id']} | {m['recall']:.3f} | {m['hit_rate']:.3f} | {m['precision']:.3f} | {quality_score:.3f} | {entity_coverage:.3f} | {p.get('latency_ms', 0):.1f} | {p.get('prompt_tokens', 0)} | {p.get('completion_tokens', 0)} | {p.get('total_tokens', 0)} | {len(qm['expected'])} | {len(qm['retrieved'])} | {reason} |\n")

                f.write("\n")

                # Performance summary for this system
                perf = result["performance"]
                f.write(f"**性能汇总**:\n")
                f.write(f"- 平均延迟: {perf['avg_latency_ms']:.1f}ms\n")
                f.write(f"- 总延迟: {perf['total_latency_ms']:.1f}ms\n")
                f.write(f"- 平均 Prompt Token: {perf['avg_prompt_tokens']:.0f}\n")
                f.write(f"- 总 Prompt Token: {perf['total_prompt_tokens']}\n")
                f.write(f"- 平均 Completion Token: {perf['avg_completion_tokens']:.0f}\n")
                f.write(f"- 总 Completion Token: {perf['total_completion_tokens']}\n")
                f.write(f"- 平均总 Token: {perf['avg_total_tokens']:.0f}\n")
                f.write(f"- 总 Token: {perf['total_total_tokens']}\n")
                f.write(f"- 平均答案质量: {result.get('avg_quality_score', 0):.3f}\n")
                f.write("\n")

        # Overall comparison
        f.write("## 总体对比\n\n")
        f.write("| 项目 | 系统 | 平均召回率 | 平均命中率 | 平均精确率 | 平均答案质量 | 可回答率 | 端到端成功率 | 平均充分性 | 平均正确性 | 平均事实性 | 检索差距 | 平均延迟(ms) | 平均总Token |\n")
        f.write("|------|------|-----------|-----------|-----------|------------|---------|------------|---------|---------|---------|--------|------------|-----------|\n")

        for result in all_results:
            agg = result["aggregated"]
            perf = result["performance"]
            key = f"{result['repo']}_{result['system']}"
            llm_agg = llm_eval_results.get(key, {}).get("aggregated", {}) if llm_eval_results else {}

            f.write(f"| {result['repo']} | {result['system']} | {agg.get('avg_recall', 0):.3f} | {agg.get('avg_hit_rate', 0):.3f} | {agg.get('avg_precision', 0):.3f} | {result.get('avg_quality_score', 0):.3f} | {llm_agg.get('answerable_rate', 0):.1%} | {llm_agg.get('end_to_end_success_rate', 0):.1%} | {llm_agg.get('avg_sufficiency', 0):.2f} | {llm_agg.get('avg_correctness', 0):.2f} | {llm_agg.get('avg_grounding', 0):.2f} | {llm_agg.get('retrieval_gap', 0):.2f} | {perf.get('avg_latency_ms', 0):.1f} | {perf.get('avg_total_tokens', 0):.0f} |\n")

        f.write("\n## 指标说明\n\n")
        f.write("### 检索指标\n")
        f.write("- **召回率 (Recall)**: 检索到的相关文件数 / 总相关文件数\n")
        f.write("- **命中率 (Hit Rate)**: 是否至少检索到一个相关文件 (1.0 或 0.0)\n")
        f.write("- **精确率 (Precision)**: 检索到的相关文件数 / 总检索文件数\n")
        f.write("- **答案质量 (Quality Score)**: 基于关键实体覆盖率和答案完整性的综合评分 (0.0-1.0)\n")
        f.write("- **实体覆盖率 (Entity Coverage)**: 答案中包含的期望关键实体比例\n")
        f.write("\n### LLM 评估指标\n")
        f.write("- **可回答率 (Answerable Rate)**: 检索上下文被判定为完全充分的查询比例 (sufficiency == 2)\n")
        f.write("- **端到端成功率 (End-to-end Success Rate)**: 答案既正确又完全基于上下文的查询比例 (correctness == 2 AND grounding == 2)\n")
        f.write("- **平均充分性 (Avg Sufficiency)**: 检索上下文充分性的平均分 (0-2)\n")
        f.write("- **平均正确性 (Avg Correctness)**: 答案正确性的平均分 (0-2)\n")
        f.write("- **平均事实性 (Avg Grounding)**: 答案事实性的平均分 (0-2)\n")
        f.write("- **检索差距 (Retrieval Gap)**: avg(sufficiency - correctness)，正值表示检索弱，负值表示生成弱\n")
        f.write("\n### 性能指标\n")
        f.write("- **延迟 (Latency)**: 每个查询的平均响应时间 (毫秒)\n")
        f.write("- **Token 使用**: Prompt + Completion 的总 Token 数\n")


if __name__ == "__main__":
    main()
