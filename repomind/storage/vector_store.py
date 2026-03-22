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
    def load(cls, path: str) -> "VectorStore":
        """
        Load vector store from disk.

        Args:
            path: Path to load the vector store from.

        Returns:
            Loaded VectorStore instance.
        """
        pass
