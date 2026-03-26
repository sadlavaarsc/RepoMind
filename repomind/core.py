"""
RepoMind Core - Unified interface for the repository understanding system.

This module provides a single, simplified interface to all RepoMind functionality.
"""

import os
import time
from typing import Dict, Any, List, Optional, Callable, TypeVar, Tuple
from functools import wraps
from pathlib import Path

from repomind.configs.settings import Settings, get_settings
from repomind.ingestion.chunker import Chunker
from repomind.indexing.embedding_service import EmbeddingService
from repomind.storage.faiss_store import FAISSStore
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.query_classifier import QueryClassifier
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker
from repomind.retrieval.pipeline import RetrievalPipeline
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind.ingestion.summary_generator import SummaryGenerator


# Type variable for timing decorator
T = TypeVar('T')


def _timing(timings_dict: Dict[str, float], key: str) -> Callable:
    """
    Decorator to measure function execution time and store in timings_dict.

    Args:
        timings_dict: Dictionary to store timing results (in ms)
        key: Key to use for storing the timing

    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            timings_dict[key] = (end - start) * 1000
            return result
        return wrapper
    return decorator


class RepoMind:
    """
    Unified RepoMind interface with configurable options.

    This class wraps all RepoMind functionality into a single, easy-to-use interface.
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        enable_query_expansion: Optional[bool] = None,
        enable_query_classification: Optional[bool] = None,
        query_expansion_variants: Optional[int] = None,
        use_fast_llm_for_expansion: bool = True,
        use_hybrid_answer_generation: bool = True,
    ):
        """
        Initialize RepoMind with configurable options.

        Args:
            settings: Optional settings object (uses get_settings() if not provided)
            enable_query_expansion: Override settings for query expansion
            enable_query_classification: Override settings for query classification
            query_expansion_variants: Override number of query expansion variants
            use_fast_llm_for_expansion: Whether to use fast LLM for query expansion
            use_hybrid_answer_generation: Whether to use hybrid (simple/fast + complex/strong) answer generation
        """
        self.settings = settings or get_settings()

        # Configurable options
        self.enable_query_expansion = enable_query_expansion if enable_query_expansion is not None else self.settings.enable_query_expansion
        self.enable_query_classification = enable_query_classification if enable_query_classification is not None else self.settings.enable_query_classification
        self.query_expansion_variants = query_expansion_variants or self.settings.query_expansion_variants
        self.use_fast_llm_for_expansion = use_fast_llm_for_expansion
        self.use_hybrid_answer_generation = use_hybrid_answer_generation

        # Initialize services
        self._init_services()

        # State
        self._is_indexed = False

    def _init_services(self) -> None:
        """Initialize all internal services."""
        # Embedding service
        self.embedding_service = EmbeddingService(
            api_key=self.settings.qwen_api_key,
            base_url=self.settings.base_url,
            model=self.settings.embedding_model
        )

        # LLM services (strong and fast)
        self.llm_service_strong = LLMService(
            api_key=self.settings.qwen_api_key,
            base_url=self.settings.base_url,
            model=self.settings.llm_model
        )

        self.llm_service_fast = LLMService(
            api_key=self.settings.qwen_api_key,
            base_url=self.settings.base_url,
            model=self.settings.llm_model_fast
        )

        # Chunker and vector store
        self.chunker = Chunker()
        self.vector_store = FAISSStore(embedding_service=self.embedding_service)

        # Summary Generator (for LLM-based chunk summaries)
        self.summary_generator = SummaryGenerator(
            api_key=self.settings.qwen_api_key,
            base_url=self.settings.base_url,
            model=self.settings.llm_model_fast
        )

        # Query Expander (uses fast LLM if enabled)
        expander_model = self.settings.llm_model_fast if self.use_fast_llm_for_expansion else self.settings.llm_model
        self.query_expander = QueryExpander(
            api_key=self.settings.qwen_api_key,
            base_url=self.settings.base_url,
            model=expander_model
        )

        # Query Classifier (uses fast LLM)
        self.query_classifier = QueryClassifier(
            api_key=self.settings.qwen_api_key,
            base_url=self.settings.base_url,
            model=self.settings.llm_model_fast
        )

        # Retrieval Pipeline (wrapped for conditional expansion)
        self.metadata_filter = MetadataFilter()
        self.reranker = Reranker(
            alpha=self.settings.rerank_alpha,
            beta=self.settings.rerank_beta,
            lambda_=getattr(self.settings, "rerank_lambda", 0.75),
            doc_bias=getattr(self.settings, "rerank_doc_bias", 0.05),
            min_doc_count=getattr(self.settings, "rerank_min_doc_count", 1),
            min_code_count=getattr(self.settings, "rerank_min_code_count", 1),
            embedding_service=self.embedding_service,
        )
        self.context_packer = ContextPacker(
            max_tokens=self.settings.max_context_tokens
        )

        # Answer Generator (supports both LLMs)
        self.answer_generator = AnswerGenerator(
            llm_service=self.llm_service_strong,
            llm_service_fast=self.llm_service_fast
        )

    def index_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Index a repository.

        Args:
            repo_path: Path to the repository to index.

        Returns:
            Dictionary with indexing result.
        """
        start_time = time.time()

        repo_path_obj = Path(repo_path)
        if not repo_path_obj.exists():
            return {
                "success": False,
                "message": f"Repository path does not exist: {repo_path}",
                "num_chunks": 0,
                "latency_ms": 0.0
            }

        chunks = self.chunker.chunk_repository(repo_path)

        if chunks:
            # Generate LLM summaries for chunks
            print(f"Generating LLM summaries for {len(chunks)} chunks...")
            chunks, _ = self.summary_generator.batch_generate_summaries(chunks)

            # Embed using the enhanced text (with structured data and summaries)
            texts = [chunk.get_embedding_text() for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)

        self._is_indexed = True

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        return {
            "success": True,
            "message": "Index built successfully",
            "num_chunks": len(chunks),
            "latency_ms": latency_ms
        }

    def save_index(self, index_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Save the index to disk.

        Args:
            index_path: Optional path to save the index (uses settings if not provided).

        Returns:
            Dictionary with save result.
        """
        path = index_path or self.settings.vector_store_path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.vector_store.save(path)
        return {
            "success": True,
            "message": "Index saved successfully",
            "index_path": path
        }

    def load_index(self, index_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load the index from disk.

        Args:
            index_path: Optional path to load the index from (uses settings if not provided).

        Returns:
            Dictionary with load result.
        """
        path = index_path or self.settings.vector_store_path
        if not os.path.exists(path):
            return {
                "success": False,
                "message": f"Index path does not exist: {path}",
                "num_chunks": 0
            }

        self.vector_store.load(path)
        self._is_indexed = True

        return {
            "success": True,
            "message": "Index loaded successfully",
            "num_chunks": len(self.vector_store.chunks)
        }

    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the indexed repository.

        Args:
            question: User question to answer.

        Returns:
            Dictionary with answer, sources, and metadata.
        """
        if not self._is_indexed and not self.vector_store.chunks:
            return {
                "answer": "No index available. Please index a repository first.",
                "sources": [],
                "latency_ms": 0.0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "query_type": None,
                "model_used": None,
                "detailed_timings": {}
            }

        start_time = time.time()
        timings = {}

        # Step 1: Query Classification (if enabled)
        query_type = self._classify_query(question, timings)

        # Step 2: Retrieval
        chunks, retrieval_timings = self._execute_retrieval(question)
        timings.update(retrieval_timings)

        # Step 3: Answer Generation
        result, generation_time = self._generate_answer(question, chunks, query_type)
        timings["answer_generation"] = generation_time

        end_time = time.time()
        total_latency = (end_time - start_time) * 1000
        timings["total_end_to_end"] = total_latency

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": total_latency,
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "full_prompt": result.get("full_prompt"),
            "query_type": query_type if self.enable_query_classification else None,
            "model_used": result.get("model_used", "strong"),
            "detailed_timings": timings
        }

    def _classify_query(self, question: str, timings: Dict[str, float]) -> str:
        """
        Classify query as simple or complex (if enabled).

        Args:
            question: User question
            timings: Dictionary to store timing results

        Returns:
            Query type ("simple" or "complex")
        """
        query_type = "complex"
        if self.enable_query_classification:
            t0 = time.time()
            query_type = self.query_classifier.classify(question)
            t1 = time.time()
            timings["query_classification"] = (t1 - t0) * 1000
        return query_type

    def _execute_retrieval(self, question: str) -> Tuple[List, Dict[str, float]]:
        """
        Execute retrieval with or without query expansion.

        Args:
            question: User question

        Returns:
            Tuple of (retrieved chunks, timing dictionary)
        """
        t2 = time.time()
        timings = {}

        if self.enable_query_expansion:
            chunks, retrieval_timings = self._perform_retrieval_with_expansion(question)
            timings.update(retrieval_timings)
        else:
            chunks, retrieval_timings = self._perform_simple_retrieval(question)
            timings.update(retrieval_timings)

        t3 = time.time()
        timings["retrieval_total"] = (t3 - t2) * 1000
        return chunks, timings

    def _perform_retrieval_with_expansion(self, question: str) -> Tuple[List, Dict[str, float]]:
        """
        Perform retrieval with query expansion.

        Args:
            question: User question

        Returns:
            Tuple of (retrieved chunks, timing dictionary)
        """
        timings = {}

        expanded_queries = self.query_expander.expand(question, num_variants=self.query_expansion_variants)

        num_variants = len(expanded_queries)
        adjusted_top_k = self.settings.retrieval_top_k * min(2, num_variants)
        adjusted_final_k = self.settings.retrieval_final_k * min(2, num_variants)

        embedding_time = 0.0
        search_time = 0.0
        all_results = []
        seen = set()

        for exp_query in expanded_queries:
            t_emb = time.time()
            query_embedding = self.embedding_service.embed(exp_query)
            t_emb2 = time.time()
            embedding_time += (t_emb2 - t_emb) * 1000

            t_search = time.time()
            results = self.vector_store.search(query_embedding, top_k=adjusted_top_k)
            t_search2 = time.time()
            search_time += (t_search2 - t_search) * 1000

            for chunk, score in results:
                chunk_id = chunk.get_identifier()
                if chunk_id not in seen:
                    seen.add(chunk_id)
                    all_results.append((chunk, score))

        all_results.sort(key=lambda x: x[1], reverse=True)
        timings["query_expansion"] = embedding_time + search_time

        filtered = self.metadata_filter.filter(all_results, question)
        reranked = self.reranker.rerank(filtered, question)
        chunks = self.context_packer.pack(reranked, final_k=adjusted_final_k)

        return chunks, timings

    def _perform_simple_retrieval(self, question: str) -> Tuple[List, Dict[str, float]]:
        """
        Perform simple single-query retrieval without expansion.

        Args:
            question: User question

        Returns:
            Tuple of (retrieved chunks, timing dictionary)
        """
        timings = {}

        t_emb = time.time()
        query_embedding = self.embedding_service.embed(question)
        t_emb2 = time.time()
        timings["embedding"] = (t_emb2 - t_emb) * 1000

        t_search = time.time()
        results = self.vector_store.search(query_embedding, top_k=self.settings.retrieval_top_k)
        t_search2 = time.time()
        timings["vector_search"] = (t_search2 - t_search) * 1000

        chunks = [chunk for chunk, _ in results[:self.settings.retrieval_final_k]]

        return chunks, timings

    def _generate_answer(self, question: str, chunks: List, query_type: str) -> Tuple[Dict[str, Any], float]:
        """
        Generate answer from retrieved chunks.

        Args:
            question: User question
            chunks: Retrieved chunks
            query_type: Query classification result

        Returns:
            Tuple of (result dict, generation time in ms)
        """
        t4 = time.time()

        use_fast_for_answer = False
        if self.use_hybrid_answer_generation and self.enable_query_classification:
            use_fast_for_answer = query_type == "simple"

        result = self.answer_generator.generate(
            question,
            chunks,
            use_fast_model=use_fast_for_answer
        )

        t5 = time.time()
        generation_time = (t5 - t4) * 1000

        return result, generation_time

    @property
    def is_indexed(self) -> bool:
        """Check if an index is available."""
        return self._is_indexed or len(self.vector_store.chunks) > 0

    @property
    def num_chunks(self) -> int:
        """Get the number of indexed chunks."""
        return len(self.vector_store.chunks)
