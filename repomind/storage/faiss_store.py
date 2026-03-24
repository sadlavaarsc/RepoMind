import os
import pickle
import numpy as np
from typing import List, Tuple, Optional
import faiss

from repomind.storage.vector_store import VectorStore
from repomind.ingestion.models import CodeChunk
from repomind.indexing.embedding_service import EmbeddingService


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
            "dimension": self.dimension
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
