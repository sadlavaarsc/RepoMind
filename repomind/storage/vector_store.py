from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from repomind.ingestion.models import CodeChunk


class VectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    def add(self, chunks: List[CodeChunk], embeddings: Optional[List[List[float]]] = None) -> None:
        """
        Add chunks to the vector store.

        Args:
            chunks: List of code chunks to add.
            embeddings: Optional pre-computed embeddings for the chunks.
        """
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int) -> List[Tuple[CodeChunk, float]]:
        """
        Search for similar chunks.

        Args:
            query_embedding: Embedding of the query.
            top_k: Number of results to return.

        Returns:
            List of (chunk, score) tuples, sorted by relevance (higher is better).
        """
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """
        Save vector store to disk.

        Args:
            path: Path to save the vector store.
        """
        pass

    @classmethod
    @abstractmethod
    def load(cls, path: str, embedding_service: Optional["EmbeddingService"] = None) -> "VectorStore":
        """
        Load vector store from disk.

        Args:
            path: Path to load the vector store from.
            embedding_service: Optional embedding service for recomputing embeddings.

        Returns:
            Loaded VectorStore instance.
        """
        pass

    @abstractmethod
    def delete(self, chunk_ids: List[str]) -> int:
        """
        Delete chunks by their IDs.

        Args:
            chunk_ids: List of chunk IDs to delete.

        Returns:
            Number of chunks actually deleted.
        """
        pass

    @abstractmethod
    def update(self, chunks: List[CodeChunk], embeddings: Optional[List[List[float]]] = None) -> int:
        """
        Update existing chunks (add if not exists).

        Args:
            chunks: List of code chunks to update.
            embeddings: Optional pre-computed embeddings for the chunks.

        Returns:
            Number of chunks updated.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all chunks from the vector store."""
        pass

    @abstractmethod
    def get_chunks_by_file(self, file_path: str) -> List[CodeChunk]:
        """
        Get all chunks belonging to a specific file.

        Args:
            file_path: Path to the file.

        Returns:
            List of chunks from the specified file.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Get the total number of chunks in the vector store.

        Returns:
            Number of chunks.
        """
        pass

    @classmethod
    @abstractmethod
    def exists(cls, path: str) -> bool:
        """
        Check if a vector store exists at the given path.

        Args:
            path: Path to check.

        Returns:
            True if the vector store exists, False otherwise.
        """
        pass
