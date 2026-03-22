from typing import List, Tuple
from repomind.ingestion.models import CodeChunk


class Reranker:
    """Lightweight reranker combining embedding score and keyword overlap."""

    def __init__(self, alpha: float = 0.7, beta: float = 0.3):
        self.alpha = alpha
        self.beta = beta

    def rerank(
        self,
        chunks_with_scores: List[Tuple[CodeChunk, float]],
        query: str
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Rerank chunks using combined scoring.

        Args:
            chunks_with_scores: List of (chunk, embedding_score) tuples.
            query: Original user query.

        Returns:
            Reranked list of (chunk, combined_score) tuples.
        """
        if not chunks_with_scores:
            return []

        query_lower = query.lower()
        reranked = []

        for chunk, embedding_score in chunks_with_scores:
            keyword_score = self._calculate_keyword_score(chunk, query_lower)
            combined_score = self.alpha * embedding_score + self.beta * keyword_score
            reranked.append((chunk, combined_score))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked

    def _calculate_keyword_score(self, chunk: CodeChunk, query_lower: str) -> float:
        """Calculate keyword overlap score between chunk and query."""
        score = 0.0

        file_path_lower = chunk.file_path.lower()

        if query_lower in file_path_lower:
            score += 0.3

        if chunk.function_name:
            func_name_lower = chunk.function_name.lower()
            if func_name_lower in query_lower:
                score += 0.25
            if query_lower in func_name_lower:
                score += 0.25

        if chunk.class_name:
            class_name_lower = chunk.class_name.lower()
            if class_name_lower in query_lower:
                score += 0.25
            if query_lower in class_name_lower:
                score += 0.25

        content_lower = chunk.content.lower()
        query_words = [word for word in query_lower.split() if len(word) > 2]

        if query_words:
            matches = sum(1 for word in query_words if word in content_lower)
            score += min(0.4, matches * 0.1)

        return min(1.0, score)
