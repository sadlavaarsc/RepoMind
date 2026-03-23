"""
Retrieval metrics for evaluating RAG systems.

Implements:
- Recall: Fraction of relevant chunks retrieved
- Hit Rate: Fraction of questions with at least one relevant chunk retrieved
- Precision: Fraction of retrieved chunks that are relevant
"""

from typing import List, Set, Dict, Any


class RetrievalMetrics:
    """Metrics for evaluating retrieval quality."""

    @staticmethod
    def calculate_recall(
        retrieved_chunks: List[str],
        relevant_chunks: Set[str]
    ) -> float:
        """
        Calculate recall: (number of relevant chunks retrieved) / (total relevant chunks)

        Args:
            retrieved_chunks: List of chunk identifiers retrieved
            relevant_chunks: Set of chunk identifiers that are relevant

        Returns:
            Recall score (0.0 to 1.0)
        """
        if not relevant_chunks:
            return 1.0

        retrieved_set = set(retrieved_chunks)
        relevant_retrieved = retrieved_set.intersection(relevant_chunks)
        return len(relevant_retrieved) / len(relevant_chunks)

    @staticmethod
    def calculate_hit_rate(
        retrieved_chunks: List[str],
        relevant_chunks: Set[str]
    ) -> float:
        """
        Calculate hit rate: 1.0 if any relevant chunk is retrieved, else 0.0

        Args:
            retrieved_chunks: List of chunk identifiers retrieved
            relevant_chunks: Set of chunk identifiers that are relevant

        Returns:
            Hit rate (0.0 or 1.0)
        """
        if not relevant_chunks:
            return 1.0

        retrieved_set = set(retrieved_chunks)
        return 1.0 if retrieved_set.intersection(relevant_chunks) else 0.0

    @staticmethod
    def calculate_precision(
        retrieved_chunks: List[str],
        relevant_chunks: Set[str]
    ) -> float:
        """
        Calculate precision: (number of relevant chunks retrieved) / (total retrieved chunks)

        Args:
            retrieved_chunks: List of chunk identifiers retrieved
            relevant_chunks: Set of chunk identifiers that are relevant

        Returns:
            Precision score (0.0 to 1.0)
        """
        if not retrieved_chunks:
            return 0.0

        retrieved_set = set(retrieved_chunks)
        relevant_retrieved = retrieved_set.intersection(relevant_chunks)
        return len(relevant_retrieved) / len(retrieved_chunks)

    @staticmethod
    def evaluate_single_query(
        retrieved_sources: List[str],
        expected_sources: List[str]
    ) -> Dict[str, float]:
        """
        Evaluate retrieval metrics for a single query.

        Args:
            retrieved_sources: List of source file paths retrieved
            expected_sources: List of source file paths that are relevant

        Returns:
            Dictionary with recall, hit_rate, precision
        """
        relevant_set = set(expected_sources)

        return {
            "recall": RetrievalMetrics.calculate_recall(retrieved_sources, relevant_set),
            "hit_rate": RetrievalMetrics.calculate_hit_rate(retrieved_sources, relevant_set),
            "precision": RetrievalMetrics.calculate_precision(retrieved_sources, relevant_set),
        }

    @staticmethod
    def aggregate_query_metrics(
        query_metrics_list: List[Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Aggregate metrics across multiple queries.

        Args:
            query_metrics_list: List of metrics dicts from evaluate_single_query

        Returns:
            Aggregated metrics with averages
        """
        if not query_metrics_list:
            return {}

        recalls = [m.get("recall", 0.0) for m in query_metrics_list]
        hit_rates = [m.get("hit_rate", 0.0) for m in query_metrics_list]
        precisions = [m.get("precision", 0.0) for m in query_metrics_list]

        return {
            "avg_recall": sum(recalls) / len(recalls),
            "avg_hit_rate": sum(hit_rates) / len(hit_rates),
            "avg_precision": sum(precisions) / len(precisions),
            "min_recall": min(recalls),
            "max_recall": max(recalls),
            "min_precision": min(precisions),
            "max_precision": max(precisions),
        }
