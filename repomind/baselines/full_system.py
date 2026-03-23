import time
from typing import Dict, Any
from repomind.ingestion.chunker import Chunker
from repomind.storage.vector_store import VectorStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker
from repomind.retrieval.pipeline import RetrievalPipeline


class FullSystem:
    """Full optimized system wrapper for baseline comparison."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        retrieval_pipeline: RetrievalPipeline,
        answer_generator: AnswerGenerator
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.retrieval_pipeline = retrieval_pipeline
        self.answer_generator = answer_generator
        self.chunker = Chunker()

    def index_repository(self, repo_path: str) -> None:
        """Index repository with full pipeline."""
        chunks = self.chunker.chunk_repository(repo_path)
        if chunks:
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)

    def query(self, query: str) -> Dict[str, Any]:
        """Query using full optimized system."""
        start_time = time.time()

        # Retrieval with detailed timings
        t0 = time.time()
        chunks, retrieval_timings = self.retrieval_pipeline.retrieve(query)
        t1 = time.time()

        # Answer generation
        t2 = time.time()
        result = self.answer_generator.generate(query, chunks)
        t3 = time.time()

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        # Combine all timings
        detailed_timings = retrieval_timings.copy()
        detailed_timings["answer_generation"] = (t3 - t2) * 1000
        detailed_timings["total_end_to_end"] = latency_ms

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": latency_ms,
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "full_prompt": result.get("full_prompt"),
            "detailed_timings": detailed_timings,
        }
