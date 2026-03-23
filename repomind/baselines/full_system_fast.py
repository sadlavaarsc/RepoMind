import time
from typing import Dict, Any
from repomind.ingestion.chunker import Chunker
from repomind.storage.vector_store import VectorStore
from repomind.indexing.embedding_service import EmbeddingService
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.query_classifier import QueryClassifier
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker
from repomind.retrieval.pipeline import RetrievalPipeline


class FullSystemFast:
    """Full optimized system with fast LLM for query expansion and classification."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        llm_service_strong: LLMService,
        llm_service_fast: LLMService,
        settings: Any
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.chunker = Chunker()

        # Initialize Query Expander with Fast LLM
        self.query_expander = QueryExpander(
            api_key=settings.qwen_api_key,
            base_url=settings.base_url,
            model=settings.llm_model_fast
        )

        # Initialize Query Classifier with Fast LLM
        self.query_classifier = QueryClassifier(
            api_key=settings.qwen_api_key,
            base_url=settings.base_url,
            model=settings.llm_model_fast
        )

        # Initialize Retrieval Pipeline with Fast Query Expander
        self.retrieval_pipeline = RetrievalPipeline(
            vector_store=vector_store,
            embedding_service=embedding_service,
            query_expander=self.query_expander,
            metadata_filter=MetadataFilter(),
            reranker=Reranker(alpha=settings.rerank_alpha, beta=settings.rerank_beta),
            context_packer=ContextPacker(max_tokens=settings.max_context_tokens),
            top_k=settings.retrieval_top_k,
            final_k=settings.retrieval_final_k
        )

        # Initialize Answer Generator with both LLM services
        self.answer_generator = AnswerGenerator(
            llm_service=llm_service_strong,
            llm_service_fast=llm_service_fast
        )

    def index_repository(self, repo_path: str) -> None:
        """Index repository with full pipeline."""
        chunks = self.chunker.chunk_repository(repo_path)
        if chunks:
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)
            self.vector_store.add(chunks, embeddings)

    def query(self, query: str) -> Dict[str, Any]:
        """Query using full optimized system with fast LLM."""
        start_time = time.time()
        timings = {}

        # Stage 1: Query Classification
        t0 = time.time()
        query_type = self.query_classifier.classify(query)
        t1 = time.time()
        timings["query_classification"] = (t1 - t0) * 1000

        # Stage 2: Retrieval with Fast LLM Query Expansion
        t2 = time.time()
        chunks, retrieval_timings = self.retrieval_pipeline.retrieve(query)
        t3 = time.time()
        timings.update(retrieval_timings)

        # Stage 3: Answer Generation with selected model
        t4 = time.time()
        use_fast = query_type == "simple"
        result = self.answer_generator.generate(query, chunks, use_fast_model=use_fast)
        t5 = time.time()
        timings["answer_generation"] = (t5 - t4) * 1000

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        timings["total_end_to_end"] = latency_ms

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": latency_ms,
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "full_prompt": result.get("full_prompt"),
            "detailed_timings": timings,
            "query_type": query_type,
            "model_used": result.get("model_used", "strong"),
        }
