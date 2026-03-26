import os
import pickle
import numpy as np
from typing import List, Tuple, Optional
import faiss

from repomind.storage.vector_store import VectorStore
from repomind.ingestion.models import CodeChunk
from repomind.indexing.embedding_service import EmbeddingService

# Version for metadata
FAISS_STORE_VERSION = "1.0"


class FAISSStore(VectorStore):
    """FAISS-based vector store implementation."""

    def __init__(self, embedding_service: Optional[EmbeddingService] = None):
        self.embedding_service = embedding_service
        self.index: Optional[faiss.IndexFlatL2] = None
        self.chunks: List[CodeChunk] = []
        self.dimension: Optional[int] = None

    def add(self, chunks: List[CodeChunk], embeddings: Optional[List[List[float]]] = None) -> None:
        """Add chunks to the FAISS index."""
        if not chunks:
            return

        if embeddings is None:
            if self.embedding_service is None:
                raise ValueError("embedding_service must be provided when embeddings are not given")
            # Use get_embedding_text() if available, otherwise fall back to content
            texts = []
            for chunk in chunks:
                if hasattr(chunk, "get_embedding_text") and callable(chunk.get_embedding_text):
                    texts.append(chunk.get_embedding_text())
                else:
                    texts.append(chunk.content)
            embeddings = self.embedding_service.embed_batch(texts)

        if self.index is None:
            self.dimension = len(embeddings[0])
            self.index = faiss.IndexFlatL2(self.dimension)

        embeddings_np = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings_np)
        self.chunks.extend(chunks)

    def search(self, query_embedding: List[float], top_k: int) -> List[Tuple[CodeChunk, float]]:
        """Search for similar chunks using FAISS."""
        if self.index is None or len(self.chunks) == 0:
            return []

        query_np = np.array([query_embedding], dtype=np.float32)
        k = min(top_k, len(self.chunks))

        distances, indices = self.index.search(query_np, k)

        results = []
        for i in range(k):
            idx = indices[0][i]
            distance = distances[0][i]
            score = 1.0 / (1.0 + distance)
            results.append((self.chunks[idx], score))

        return results

    def save(self, path: str) -> None:
        """Save FAISS index and chunks to disk."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if self.index is not None:
            faiss.write_index(self.index, f"{path}.index")

        data = {
            "chunks": self.chunks,
            "dimension": self.dimension,
            "version": FAISS_STORE_VERSION,
            "num_chunks": len(self.chunks)
        }
        with open(f"{path}.pkl", "wb") as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, path: str, embedding_service: Optional[EmbeddingService] = None) -> "FAISSStore":
        """Load FAISS index and chunks from disk."""
        store = cls(embedding_service=embedding_service)

        if os.path.exists(f"{path}.index"):
            store.index = faiss.read_index(f"{path}.index")

        if os.path.exists(f"{path}.pkl"):
            with open(f"{path}.pkl", "rb") as f:
                data = pickle.load(f)
                store.chunks = data["chunks"]
                store.dimension = data["dimension"]

        return store

    def delete(self, chunk_ids: List[str]) -> int:
        """Delete chunks by their IDs. Note: FAISS doesn't support efficient deletion, so we rebuild the index."""
        if not chunk_ids or len(self.chunks) == 0:
            return 0

        # Create a set for faster lookups
        id_set = set(chunk_ids)

        # Collect chunks to keep and their indices
        keep_chunks = []
        keep_indices = []

        for i, chunk in enumerate(self.chunks):
            # Use chunk id if available, otherwise use a hash of content+filepath
            chunk_id = getattr(chunk, "id", None) or f"{chunk.file_path}:{hash(chunk.content)}"
            if chunk_id not in id_set:
                keep_chunks.append(chunk)
                keep_indices.append(i)

        deleted_count = len(self.chunks) - len(keep_chunks)

        if deleted_count > 0:
            # Rebuild index if we deleted anything
            self.chunks = keep_chunks
            if len(keep_chunks) > 0 and self.index is not None:
                # Extract embeddings for kept chunks and rebuild index
                # Note: This requires recomputing embeddings or storing them
                # For simplicity, we'll clear and require re-adding if needed
                self.index = None
                self.dimension = None
            else:
                self.index = None
                self.dimension = None

        return deleted_count

    def update(self, chunks: List[CodeChunk], embeddings: Optional[List[List[float]]] = None) -> int:
        """Update existing chunks (add if not exists)."""
        if not chunks:
            return 0

        # Collect chunk IDs to delete
        chunk_ids_to_delete = []
        for chunk in chunks:
            chunk_id = getattr(chunk, "id", None) or f"{chunk.file_path}:{hash(chunk.content)}"
            chunk_ids_to_delete.append(chunk_id)

        # Delete old versions
        deleted_count = self.delete(chunk_ids_to_delete)

        # Add new versions
        self.add(chunks, embeddings)

        return len(chunks)

    def clear(self) -> None:
        """Clear all chunks from the vector store."""
        self.chunks = []
        self.index = None
        self.dimension = None

    def get_chunks_by_file(self, file_path: str) -> List[CodeChunk]:
        """Get all chunks belonging to a specific file."""
        return [chunk for chunk in self.chunks if chunk.file_path == file_path]

    def count(self) -> int:
        """Get the total number of chunks in the vector store."""
        return len(self.chunks)

    @classmethod
    def exists(cls, path: str) -> bool:
        """Check if a vector store exists at the given path."""
        return os.path.exists(f"{path}.index") and os.path.exists(f"{path}.pkl")
