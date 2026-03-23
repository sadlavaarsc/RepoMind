"""Full System Fast baseline using hybrid LLM strategy."""

from typing import Dict, Any
from repomind.core import RepoMind
from repomind.configs.settings import get_settings


class FullSystemFast:
    """Full optimized system with fast LLM for query expansion and classification."""

    def __init__(
        self,
        vector_store=None,
        embedding_service=None,
        llm_service_strong=None,
        llm_service_fast=None,
        settings=None
    ):
        """
        Initialize FullSystemFast using RepoMind core.

        The parameters are kept for backward compatibility but ignored -
        we use RepoMind core directly instead.
        """
        self.settings = settings or get_settings()
        self.repomind = RepoMind(
            enable_query_expansion=True,
            enable_query_classification=True,
            query_expansion_variants=2,
            use_fast_llm_for_expansion=True,
            use_hybrid_answer_generation=True,
        )

    def index_repository(self, repo_path: str) -> None:
        """Index repository with full pipeline."""
        self.repomind.index_repository(repo_path)

    def query(self, query: str) -> Dict[str, Any]:
        """Query using full optimized system with fast LLM."""
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
            "query_type": result.get("query_type"),
            "model_used": result.get("model_used", "strong"),
        }
