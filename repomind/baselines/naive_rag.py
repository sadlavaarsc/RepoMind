"""
Naive RAG baseline: file-level chunk, no MQE, no rerank.
"""

import time
from typing import Dict, Any
from repomind.ingestion.file_chunker import FileChunker
from repomind.ingestion.models import CodeChunk
from repomind.storage.vector_store import VectorStore
from repomind.storage.faiss_store import FAISSStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind.baselines.base import BaseRAG


class NaiveRAG(BaseRAG):
    """
    Naive RAG baseline: file-level chunk, no MQE, no rerank.

    Inherits from BaseRAG and uses FileChunker for file-level chunking.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        answer_generator: AnswerGenerator,
        top_k: int = 5
    ):
        """
        Initialize NaiveRAG.

        Args:
            vector_store: Vector store for storing/retrieving embeddings
            embedding_service: Service for generating embeddings
            answer_generator: Service for generating answers from chunks
            top_k: Number of chunks to retrieve
        """
        super().__init__(
            vector_store=vector_store,
            embedding_service=embedding_service,
            answer_generator=answer_generator,
            top_k=top_k,
            chunker=FileChunker()
        )
