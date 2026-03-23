import time
from typing import List, Dict, Any, Tuple
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

    def retrieve(self, query: str) -> Tuple[List[CodeChunk], Dict[str, float]]:
        """
        End-to-end retrieval: expand -> search -> filter -> rerank -> pack.

        Args:
            query: Original user query.

        Returns:
            Tuple of (list of relevant code chunks, dict of stage timings in ms).
        """
        timings = {}

        # Stage 1: Query Expansion
        t0 = time.time()
        expanded_queries = self.query_expander.expand(query, num_variants=2)
        t1 = time.time()
        timings["query_expansion"] = (t1 - t0) * 1000

        # Stage 2: Vector Search (multiple queries)
        t2 = time.time()
        all_results = []
        seen = set()

        # Batch embedding for all queries at once (optimization)
        t_emb_start = time.time()
        query_embeddings = self.embedding_service.embed_batch(expanded_queries)
        t_emb_end = time.time()
        embedding_time = (t_emb_end - t_emb_start) * 1000

        # Vector search for each query
        search_time = 0.0
        for exp_query, query_embedding in zip(expanded_queries, query_embeddings):
            t_search_start = time.time()
            results = self.vector_store.search(query_embedding, top_k=self.top_k)
            t_search_end = time.time()
            search_time += (t_search_end - t_search_start) * 1000

            for chunk, score in results:
                chunk_id = chunk.get_identifier()
                if chunk_id not in seen:
                    seen.add(chunk_id)
                    all_results.append((chunk, score))

        all_results.sort(key=lambda x: x[1], reverse=True)
        t3 = time.time()
        timings["embedding"] = embedding_time
        timings["vector_search"] = search_time
        timings["result_merge"] = (t3 - t2) * 1000 - embedding_time - search_time

        # Stage 3: Metadata Filter
        t4 = time.time()
        filtered = self.metadata_filter.filter(all_results, query)
        t5 = time.time()
        timings["metadata_filter"] = (t5 - t4) * 1000

        # Stage 4: Reranking
        t6 = time.time()
        reranked = self.reranker.rerank(filtered, query)
        t7 = time.time()
        timings["reranking"] = (t7 - t6) * 1000

        # Stage 5: Context Packing
        t8 = time.time()
        packed = self.context_packer.pack(reranked, final_k=self.final_k)
        t9 = time.time()
        timings["context_packing"] = (t9 - t8) * 1000

        # Total retrieval time
        timings["total_retrieval"] = (t9 - t0) * 1000

        return packed, timings
