"""
Structured RAG baseline: function-level chunk, but no MQE/rerank.
"""

import time
from typing import Dict, Any
from repomind.ingestion.chunker import Chunker
from repomind.ingestion.summary_generator import SummaryGenerator
from repomind.storage.vector_store import VectorStore
from repomind.storage.faiss_store import FAISSStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind.baselines.base import BaseRAG


class StructuredRAG(BaseRAG):
    """
    Structured RAG baseline: function-level chunk, but no MQE/rerank.

    Inherits from BaseRAG and uses Chunker for function-level chunking,
    with optional SummaryGenerator for LLM summaries.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        answer_generator: AnswerGenerator,
        top_k: int = 5,
        summary_generator: SummaryGenerator = None
    ):
        """
        Initialize StructuredRAG.

        Args:
            vector_store: Vector store for storing/retrieving embeddings
            embedding_service: Service for generating embeddings
            answer_generator: Service for generating answers from chunks
            top_k: Number of chunks to retrieve
            summary_generator: Optional summary generator for LLM summaries
        """
        super().__init__(
            vector_store=vector_store,
            embedding_service=embedding_service,
            answer_generator=answer_generator,
            top_k=top_k,
            chunker=Chunker()
        )
        self.summary_generator = summary_generator

    def index_repository(self, repo_path: str) -> None:
        """
        Index repository with function-level chunks and optional LLM summaries.

        Overrides BaseRAG.index_repository to add summary generation support.

        Args:
            repo_path: Path to the repository to index
        """
        chunks = self.chunker.chunk_repository(repo_path)
        if chunks:
            # Generate LLM summaries if summary generator is available
            if self.summary_generator:
                print(f"Generating LLM summaries for {len(chunks)} chunks...")
                chunks, _ = self.summary_generator.batch_generate_summaries(chunks)

            texts = [chunk.get_embedding_text() for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)
