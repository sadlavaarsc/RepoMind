import time
from typing import Dict, Any, List
from repomind.ingestion.file_chunker import FileChunker
from repomind.ingestion.models import CodeChunk
from repomind.storage.vector_store import VectorStore
from repomind.storage.faiss_store import FAISSStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator


class NaiveRAG:
    """Naive RAG baseline: file-level chunk, no MQE, no rerank."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        answer_generator: AnswerGenerator,
        top_k: int = 5
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.answer_generator = answer_generator
        self.top_k = top_k
        self.chunker = FileChunker()

    def index_repository(self, repo_path: str) -> None:
        """Index repository with file-level chunks."""
        chunks = self.chunker.chunk_repository(repo_path)
        if chunks:
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)

    def query(self, query: str) -> Dict[str, Any]:
        """Query using naive RAG approach."""
        start_time = time.time()

        query_embedding = self.embedding_service.embed(query)
        results = self.vector_store.search(query_embedding, top_k=self.top_k)

        chunks = [chunk for chunk, _ in results]

        result = self.answer_generator.generate(query, chunks)

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": latency_ms,
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "full_prompt": result.get("full_prompt"),
        }
