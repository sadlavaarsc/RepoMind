from typing import List
from openai import OpenAI


class EmbeddingService:
    """Service for generating embeddings using OpenAI-compatible API."""

    # Qwen 嵌入模型限制：一次最多 10 个
    MAX_BATCH_SIZE = 10

    def __init__(self, api_key: str, base_url: str, model: str = "text-embedding-v4"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def embed(self, text: str) -> List[float]:
        """
        Embed a single text string.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector as a list of floats.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts with automatic batching (max 10 per request).

        Args:
            texts: List of texts to embed.

        Returns:
            List of embedding vectors.
        """
        all_embeddings = []

        # 分批处理，每批不超过 MAX_BATCH_SIZE
        for i in range(0, len(texts), self.MAX_BATCH_SIZE):
            batch = texts[i:i + self.MAX_BATCH_SIZE]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings
