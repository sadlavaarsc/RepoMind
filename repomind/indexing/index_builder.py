from typing import Optional
from repomind.ingestion.chunker import Chunker
from repomind.storage.vector_store import VectorStore
from repomind.indexing.embedding_service import EmbeddingService


class IndexBuilder:
    """Orchestrates building a search index from a repository."""

    def __init__(
        self,
        chunker: Chunker,
        vector_store: VectorStore,
        embedding_service: EmbeddingService
    ):
        self.chunker = chunker
        self.vector_store = vector_store
        self.embedding_service = embedding_service

    def build_index(self, repo_path: str) -> None:
        """
        Build an index from a repository.

        Args:
            repo_path: Path to the repository to index.
        """
        chunks = self.chunker.chunk_repository(repo_path)
        if chunks:
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)

    def save_index(self, path: str) -> None:
        """Save the built index to disk."""
        self.vector_store.save(path)

    @classmethod
    def load_index(
        cls,
        path: str,
        chunker: Chunker,
        vector_store: VectorStore,
        embedding_service: EmbeddingService
    ) -> "IndexBuilder":
        """Load a previously saved index."""
        loaded_store = vector_store.__class__.load(path, embedding_service=embedding_service)
        return cls(chunker, loaded_store, embedding_service)
