#!/usr/bin/env python
"""
Run full LLM evaluation on all baseline results.

Supports model selection via command line argument.
"""

import sys
import asyncio
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.evaluation.result_parser import (
    parse_comparison_report,
    parse_prompt_file,
    find_prompt_file
)
from repomind.evaluation.llm_evaluator import LLMEvaluator
from repomind.evaluation.llm_metrics import aggregate_llm_metrics


async def evaluate_query(
    evaluator: LLMEvaluator,
    query_id: int,
    question_data: Dict[str, Any],
    comparison_data: Dict[str, Any],
    retrieved_context: str
) -> Dict[str, Any]:
    """Evaluate a single query."""
    result = await evaluator.evaluate_single_query(
        query=comparison_data["question"],
        retrieved_context=retrieved_context,
        pred_answer=comparison_data["pred_answer"],
        gold_answer=question_data["reference_answer"]
    )

    return {
        "query_id": query_id,
        "question": comparison_data["question"],
        "pred_answer": comparison_data["pred_answer"],
        "gold_answer": question_data["reference_answer"],
        "evaluation": result
    }


async def evaluate_system(
    repo_name: str,
    system_name: str,
    test_suite_dir: Path,
    results_archive_dir: Path,
    output_dir: Path,
    model: str,
    results_dir_suffix: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate a single system.

    Args:
        repo_name: Name of the repository (travel_agent or cuezero)
        system_name: Name of the system (e.g., structured_rag_new_chunk_llm_summary_fixed)
        test_suite_dir: Path to test suite directory
        results_archive_dir: Path to results archive directory
        output_dir: Path to output directory
        model: Model to use for evaluation
        results_dir_suffix: Optional suffix for the results directory (for multi-system reports).
            If provided, the report path will be results_archive_dir / f"baseline_results_{results_dir_suffix}"
            instead of results_archive_dir / f"baseline_results_{repo_name}_{system_name}".
            This is used for multi-system reports where multiple systems share the same directory.
    """
    print(f"\n{'=' * 80}")
    print(f"Evaluating: {repo_name} - {system_name} (model: {model})")
    print(f"{'=' * 80}")

    evaluator = LLMEvaluator(model=model)

    # Load test suite
    test_suite_path = test_suite_dir / repo_name / "test_questions.json"
    with open(test_suite_path, "r", encoding="utf-8") as f:
        test_suite = json.load(f)
    question_lookup = {q["id"]: q for q in test_suite["questions"]}

    # Determine report path
    if results_dir_suffix:
        report_path = results_archive_dir / f"baseline_results_{results_dir_suffix}" / "comparison_report.md"
        # For multi-system reports, we need to map system names to display names
        display_name_map = {
            "structured_rag_new_chunk_llm_summary_fixed": "Structured RAG",
            "full_system_new_chunk_llm_summary_fixed": "Full System",
            "full_system_fast_new_chunk_llm_summary_fixed": "Full System Fast",
            "full_system_new_rerank": "Full System",
            "full_system_fast_new_rerank": "Full System Fast",
            "full_system_chinese_rerank_fix": "Full System",
            "full_system_fast_chinese_rerank_fix": "Full System Fast",
        }
        target_display_name = display_name_map.get(system_name, system_name.replace("_", " ").title())
    else:
        report_path = results_archive_dir / f"baseline_results_{repo_name}_{system_name}" / "comparison_report.md"
        target_display_name = None

    # Load comparison report
    comparison_data = parse_comparison_report(report_path, target_system=target_display_name)

    # Load prompts dir (use the same dir as report)
    if results_dir_suffix:
        prompts_dir = results_archive_dir / f"baseline_results_{results_dir_suffix}" / "prompts"
    else:
        prompts_dir = results_archive_dir / f"baseline_results_{repo_name}_{system_name}" / "prompts"

    # Evaluate each query
    query_evals = {}
    for query_id in sorted(comparison_data.keys()):
        if query_id not in question_lookup:
            continue

        print(f"\n--- Query {query_id}/10 ---")

        question_data = question_lookup[query_id]
        query_comp_data = comparison_data[query_id]

        # Get retrieved context
        prompt_file = find_prompt_file(prompts_dir, query_id)
        retrieved_context = ""
        if prompt_file:
            _, retrieved_context = parse_prompt_file(prompt_file)

        # Evaluate
        eval_result = await evaluate_query(
            evaluator=evaluator,
            query_id=query_id,
            question_data=question_data,
            comparison_data=query_comp_data,
            retrieved_context=retrieved_context
        )
        query_evals[query_id] = eval_result

        # Print immediate result
        eval = eval_result["evaluation"]
        print(f"  Sufficiency: {eval['sufficiency']['score']}")
        print(f"  Correctness: {eval['correctness']['score']}")
        print(f"  Grounding: {eval['grounding']['score']}")

    # Calculate aggregate metrics
    result = {
        "repo": repo_name,
        "system": system_name,
        "model": model,
        "query_evals": query_evals
    }
    aggregated = aggregate_llm_metrics(query_evals)
    result["aggregated"] = aggregated

    # Save raw results
    output_file = output_dir / f"llm_eval_{repo_name}_{system_name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Results saved to: {output_file}")

    # Print summary
    print(f"\n{'-' * 80}")
    print(f"Summary for {repo_name} - {system_name}:")
    print(f"{'-' * 80}")
    print(f"  Number of queries: {aggregated['num_queries']}")
    print(f"  Answerable rate: {aggregated['answerable_rate']:.1%}")
    print(f"  End-to-end success rate: {aggregated['end_to_end_success_rate']:.1%}")
    print(f"  Avg sufficiency: {aggregated['avg_sufficiency']:.2f}")
    print(f"  Avg correctness: {aggregated['avg_correctness']:.2f}")
    print(f"  Avg grounding: {aggregated['avg_grounding']:.2f}")
    print(f"  Retrieval gap: {aggregated['retrieval_gap']:.2f}")

    return result


async def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(description="Run LLM evaluation on baseline results.")
    parser.add_argument("--model", type=str, default="qwen-flash",
                        help="Model to use for evaluation (default: qwen-flash)")
    parser.add_argument("--systems", type=str, nargs="+", default=None,
                        help="Specific systems to evaluate (default: all)")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    test_suite_dir = repo_root / "test_suite"
    results_archive_dir = repo_root / "baseline_results_archive"
    output_dir = repo_root / "llm_evaluation_results"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # All systems to evaluate - tuple format:
    # (repo_name, system_name, results_dir_suffix)
    # If results_dir_suffix is provided, it will be used instead of repo_name_system_name
    all_systems = [
        ("travel_agent", "llm_only", None),
        ("travel_agent", "naive_rag", None),
        ("travel_agent", "structured_rag", None),
        ("travel_agent", "structured_rag_new_chunk", None),
        ("travel_agent", "full_system", None),
        ("travel_agent", "full_system_fast", None),
        ("travel_agent", "full_system_new_chunk", None),
        ("travel_agent", "full_system_fast_new_chunk", None),
        ("travel_agent", "full_system_new_chunk_bilingual", None),
        ("travel_agent", "full_system_fast_new_chunk_bilingual", None),
        ("cuezero", "llm_only", None),
        ("cuezero", "naive_rag", None),
        ("cuezero", "structured_rag", None),
        ("cuezero", "structured_rag_new_chunk", None),
        ("cuezero", "full_system", None),
        ("cuezero", "full_system_fast", None),
        ("cuezero", "full_system_new_chunk", None),
        ("cuezero", "full_system_fast_new_chunk", None),
        ("cuezero", "full_system_new_chunk_bilingual", None),
        ("cuezero", "full_system_fast_new_chunk_bilingual", None),
        # Multi-system reports (llm_summary versions - cuezero only)
        ("cuezero", "structured_rag_new_chunk_llm_summary", "cuezero_full_system_new_chunk_llm_summary"),
        ("cuezero", "full_system_new_chunk_llm_summary", "cuezero_full_system_new_chunk_llm_summary"),
        ("cuezero", "full_system_fast_new_chunk_llm_summary", "cuezero_full_system_new_chunk_llm_summary"),
        # Multi-system reports (fixed versions)
        ("travel_agent", "structured_rag_new_chunk_llm_summary_fixed", "travel_agent_new_chunk_llm_summary_fixed"),
        ("travel_agent", "full_system_new_chunk_llm_summary_fixed", "travel_agent_new_chunk_llm_summary_fixed"),
        ("travel_agent", "full_system_fast_new_chunk_llm_summary_fixed", "travel_agent_new_chunk_llm_summary_fixed"),
        ("cuezero", "structured_rag_new_chunk_llm_summary_fixed", "cuezero_new_chunk_llm_summary_fixed"),
        ("cuezero", "full_system_new_chunk_llm_summary_fixed", "cuezero_new_chunk_llm_summary_fixed"),
        ("cuezero", "full_system_fast_new_chunk_llm_summary_fixed", "cuezero_new_chunk_llm_summary_fixed"),
        # Multi-system reports (new_rerank versions)
        ("travel_agent", "full_system_new_rerank", "travel_agent_new_rerank"),
        ("travel_agent", "full_system_fast_new_rerank", "travel_agent_new_rerank"),
        ("cuezero", "full_system_new_rerank", "cuezero_new_rerank"),
        ("cuezero", "full_system_fast_new_rerank", "cuezero_new_rerank"),
        # Multi-system reports (chinese_rerank_fix versions)
        ("travel_agent", "full_system_chinese_rerank_fix", "travel_agent_chinese_rerank_fix"),
        ("travel_agent", "full_system_fast_chinese_rerank_fix", "travel_agent_chinese_rerank_fix"),
        ("cuezero", "full_system_chinese_rerank_fix", "cuezero_chinese_rerank_fix"),
        ("cuezero", "full_system_fast_chinese_rerank_fix", "cuezero_chinese_rerank_fix"),
    ]

    # Filter if specific systems are requested
    if args.systems:
        systems_to_eval = []
        for repo_name, system_name, dir_suffix in all_systems:
            key = f"{repo_name}_{system_name}"
            if key in args.systems or system_name in args.systems:
                systems_to_eval.append((repo_name, system_name, dir_suffix))
    else:
        systems_to_eval = all_systems

    print(f"Will evaluate {len(systems_to_eval)} systems")
    print(f"Using model: {args.model}")

    all_results = {}

    for repo_name, system_name, dir_suffix in systems_to_eval:
        try:
            result = await evaluate_system(
                repo_name=repo_name,
                system_name=system_name,
                test_suite_dir=test_suite_dir,
                results_archive_dir=results_archive_dir,
                output_dir=output_dir,
                model=args.model,
                results_dir_suffix=dir_suffix
            )
            all_results[f"{repo_name}_{system_name}"] = result
        except Exception as e:
            print(f"\n✗ Failed to evaluate {repo_name} - {system_name}: {e}")
            import traceback
            traceback.print_exc()

    # Save summary
    summary_file = output_dir / "llm_eval_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Evaluation complete! Summary saved to: {summary_file}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    asyncio.run(main())
