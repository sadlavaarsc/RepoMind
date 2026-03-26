"""
Base class for RAG baselines with common functionality.
"""

import time
from typing import Dict, Any, List, Optional
from repomind.ingestion.models import CodeChunk
from repomind.storage.vector_store import VectorStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.generation.answer_generator import AnswerGenerator


class BaseRAG:
    """
    Base class for RAG baselines with common functionality.

    Provides shared initialization, indexing, and query logic that can be
    reused by concrete RAG implementations.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        answer_generator: AnswerGenerator,
        top_k: int = 5,
        chunker = None
    ):
        """
        Initialize BaseRAG.

        Args:
            vector_store: Vector store for storing/retrieving embeddings
            embedding_service: Service for generating embeddings
            answer_generator: Service for generating answers from chunks
            top_k: Number of chunks to retrieve
            chunker: Optional chunker for indexing (if None, subclasses should set it)
        """
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.answer_generator = answer_generator
        self.top_k = top_k
        self.chunker = chunker

    def index_repository(self, repo_path: str) -> None:
        """
        Index a repository using the configured chunker.

        Subclasses can override this to customize indexing behavior.

        Args:
            repo_path: Path to the repository to index
        """
        if self.chunker is None:
            raise ValueError("Chunker must be set before calling index_repository")

        chunks = self.chunker.chunk_repository(repo_path)
        if chunks:
            texts = [chunk.get_embedding_text() for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)

    def _retrieve_chunks(self, query: str) -> List[CodeChunk]:
        """
        Retrieve relevant chunks for a query.

        Subclasses can override this to customize retrieval logic.

        Args:
            query: User query

        Returns:
            List of retrieved code chunks
        """
        query_embedding = self.embedding_service.embed(query)
        results = self.vector_store.search(query_embedding, top_k=self.top_k)
        return [chunk for chunk, _ in results]

    def query(self, query: str) -> Dict[str, Any]:
        """
        Query the RAG system.

        This is the main entry point that orchestrates retrieval and answer generation.

        Args:
            query: User query

        Returns:
            Dictionary with answer, sources, latency, and token usage
        """
        start_time = time.time()

        chunks = self._retrieve_chunks(query)
        result = self.answer_generator.generate(query, chunks)

        latency_ms = (time.time() - start_time) * 1000

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": latency_ms,
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "full_prompt": result.get("full_prompt"),
        }
