from typing import List
from repomind.ingestion.models import CodeChunk
from repomind.storage.vector_store import VectorStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker


class RetrievalPipeline:
    """End-to-end retrieval pipeline with multiple stages."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        query_expander: QueryExpander,
        metadata_filter: MetadataFilter,
        reranker: Reranker,
        context_packer: ContextPacker,
        top_k: int = 20,
        final_k: int = 5
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.query_expander = query_expander
        self.metadata_filter = metadata_filter
        self.reranker = reranker
        self.context_packer = context_packer
        self.top_k = top_k
        self.final_k = final_k

    def retrieve(self, query: str) -> List[CodeChunk]:
        """
        End-to-end retrieval: expand -> search -> filter -> rerank -> pack.

        Args:
            query: Original user query.

        Returns:
            List of relevant code chunks.
        """
        expanded_queries = self.query_expander.expand(query, num_variants=2)

        all_results = []
        seen = set()

        for exp_query in expanded_queries:
            query_embedding = self.embedding_service.embed(exp_query)
            results = self.vector_store.search(query_embedding, top_k=self.top_k)

            for chunk, score in results:
                chunk_id = chunk.get_identifier()
                if chunk_id not in seen:
                    seen.add(chunk_id)
                    all_results.append((chunk, score))

        all_results.sort(key=lambda x: x[1], reverse=True)

        filtered = self.metadata_filter.filter(all_results, query)

        reranked = self.reranker.rerank(filtered, query)

        packed = self.context_packer.pack(reranked, final_k=self.final_k)

        return packed
