import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from repomind.api.schemas import (
    IndexRequest, IndexResponse, QueryRequest, QueryResponse, HealthResponse
)
from repomind.configs.settings import get_settings
from repomind.ingestion.chunker import Chunker
from repomind.indexing.embedding_service import EmbeddingService
from repomind.indexing.index_builder import IndexBuilder
from repomind.storage.faiss_store import FAISSStore
from repomind.retrieval.query_expander import QueryExpander
from repomind.retrieval.metadata_filter import MetadataFilter
from repomind.retrieval.reranker import Reranker
from repomind.retrieval.context_packer import ContextPacker
from repomind.retrieval.pipeline import RetrievalPipeline
from repomind.generation.llm_service import LLMService
from repomind.generation.answer_generator import AnswerGenerator
from repomind import __version__


# Global state
index_builder: IndexBuilder = None
retrieval_pipeline: RetrievalPipeline = None
answer_generator: AnswerGenerator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on app startup."""
    global index_builder, retrieval_pipeline, answer_generator

    settings = get_settings()

    embedding_service = EmbeddingService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.embedding_model
    )

    llm_service = LLMService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model
    )

    chunker = Chunker()
    vector_store = FAISSStore(embedding_service=embedding_service)
    index_builder = IndexBuilder(chunker, vector_store, embedding_service)

    query_expander = QueryExpander(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.llm_model
    )

    retrieval_pipeline = RetrievalPipeline(
        vector_store=vector_store,
        embedding_service=embedding_service,
        query_expander=query_expander,
        metadata_filter=MetadataFilter(),
        reranker=Reranker(alpha=settings.rerank_alpha, beta=settings.rerank_beta),
        context_packer=ContextPacker(max_tokens=settings.max_context_tokens),
        top_k=settings.retrieval_top_k,
        final_k=settings.retrieval_final_k
    )

    answer_generator = AnswerGenerator(llm_service=llm_service)

    yield

    index_builder = None
    retrieval_pipeline = None
    answer_generator = None


app = FastAPI(
    title="RepoMind API",
    description="Code-aware RAG system for repository understanding",
    version=__version__,
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version=__version__)


@app.post("/index", response_model=IndexResponse)
async def index_repository(request: IndexRequest):
    """Index a repository."""
    global index_builder

    if not index_builder:
        raise HTTPException(status_code=500, detail="Service not initialized")

    if not os.path.exists(request.repo_path):
        raise HTTPException(status_code=400, detail="Repository path does not exist")

    try:
        index_builder.build_index(request.repo_path)

        settings = get_settings()
        os.makedirs(os.path.dirname(settings.vector_store_path), exist_ok=True)
        index_builder.save_index(settings.vector_store_path)

        num_chunks = len(index_builder.vector_store.chunks)

        return IndexResponse(
            success=True,
            message="Index built successfully",
            num_chunks=num_chunks,
            index_path=settings.vector_store_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index repository: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_repository(request: QueryRequest):
    """Query the indexed repository."""
    global retrieval_pipeline, answer_generator

    if not retrieval_pipeline or not answer_generator:
        raise HTTPException(status_code=500, detail="Service not initialized")

    if not retrieval_pipeline.vector_store.chunks:
        raise HTTPException(status_code=400, detail="No index available. Please index a repository first.")

    try:
        start_time = time.time()
        chunks = retrieval_pipeline.retrieve(request.question)
        result = answer_generator.generate(request.question, chunks)
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency_ms=latency_ms,
            prompt_tokens=result.get("prompt_tokens"),
            completion_tokens=result.get("completion_tokens"),
            total_tokens=result.get("total_tokens"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query: {str(e)}")
