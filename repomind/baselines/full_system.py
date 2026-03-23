"""Full System baseline using strong LLM for everything."""

from typing import Dict, Any
from repomind.core import RepoMind
from repomind.configs.settings import get_settings


class FullSystem:
    """Full optimized system wrapper for baseline comparison."""

    def __init__(
        self,
        vector_store=None,
        embedding_service=None,
        retrieval_pipeline=None,
        answer_generator=None
    ):
        """
        Initialize FullSystem using RepoMind core.

        The parameters are kept for backward compatibility but ignored -
        we use RepoMind core directly instead.
        """
        self.settings = get_settings()
        self.repomind = RepoMind(
            enable_query_expansion=True,
            enable_query_classification=False,
            query_expansion_variants=2,
            use_fast_llm_for_expansion=False,
            use_hybrid_answer_generation=False,
        )

    def index_repository(self, repo_path: str) -> None:
        """Index repository with full pipeline."""
        self.repomind.index_repository(repo_path)

    def query(self, query: str) -> Dict[str, Any]:
        """Query using full optimized system."""
        result = self.repomind.query(query)
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": result["latency_ms"],
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "full_prompt": result.get("full_prompt"),
            "detailed_timings": result.get("detailed_timings", {}),
        }
