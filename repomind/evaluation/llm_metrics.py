"""
Aggregate LLM evaluation metrics.

Calculates:
- answerable_rate
- end_to_end_success_rate
- avg_sufficiency
- avg_correctness
- avg_grounding
- retrieval_gap
"""

from typing import Dict, Any, List


def aggregate_llm_metrics(query_evals: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate LLM evaluation metrics from query evaluations.

    Args:
        query_evals: {query_id: query_eval_data}

    Returns:
        Aggregated metrics dictionary
    """
    if not query_evals:
        return {}

    sufficiency_scores = []
    correctness_scores = []
    grounding_scores = []

    answerable_count = 0
    end_to_end_success_count = 0

    for query_eval in query_evals.values():
        evaluation = query_eval.get("evaluation", {})

        # Extract scores
        sufficiency = evaluation.get("sufficiency", {})
        correctness = evaluation.get("correctness", {})
        grounding = evaluation.get("grounding", {})

        suff_score = sufficiency.get("score", 0)
        corr_score = correctness.get("score", 0)
        ground_score = grounding.get("score", 0)

        sufficiency_scores.append(suff_score)
        correctness_scores.append(corr_score)
        grounding_scores.append(ground_score)

        # Count answerable (sufficiency == 2)
        if suff_score == 2:
            answerable_count += 1

        # Count end-to-end success (correctness == 2 AND grounding == 2)
        if corr_score == 2 and ground_score == 2:
            end_to_end_success_count += 1

    num_queries = len(query_evals)

    # Calculate averages
    avg_sufficiency = sum(sufficiency_scores) / num_queries if num_queries > 0 else 0
    avg_correctness = sum(correctness_scores) / num_queries if num_queries > 0 else 0
    avg_grounding = sum(grounding_scores) / num_queries if num_queries > 0 else 0

    # Calculate rates
    answerable_rate = answerable_count / num_queries if num_queries > 0 else 0
    end_to_end_success_rate = end_to_end_success_count / num_queries if num_queries > 0 else 0

    # Calculate retrieval gap: avg(sufficiency - correctness)
    retrieval_gap = avg_sufficiency - avg_correctness

    return {
        "num_queries": num_queries,
        "answerable_rate": answerable_rate,
        "end_to_end_success_rate": end_to_end_success_rate,
        "avg_sufficiency": avg_sufficiency,
        "avg_correctness": avg_correctness,
        "avg_grounding": avg_grounding,
        "retrieval_gap": retrieval_gap,
        "answerable_count": answerable_count,
        "end_to_end_success_count": end_to_end_success_count,
    }
