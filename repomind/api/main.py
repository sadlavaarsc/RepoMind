import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from repomind.api.schemas import (
    IndexRequest, IndexResponse, QueryRequest, QueryResponse, HealthResponse
)
from repomind.configs.settings import get_settings
from repomind.core import RepoMind
from repomind import __version__


# Global state
repomind: RepoMind = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize RepoMind on app startup."""
    global repomind

    repomind = RepoMind()

    yield

    repomind = None


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
    global repomind

    if not repomind:
        raise HTTPException(status_code=500, detail="Service not initialized")

    if not os.path.exists(request.repo_path):
        raise HTTPException(status_code=400, detail="Repository path does not exist")

    try:
        result = repomind.index_repository(request.repo_path)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])

        save_result = repomind.save_index()

        return IndexResponse(
            success=True,
            message="Index built successfully",
            num_chunks=result["num_chunks"],
            index_path=save_result["index_path"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index repository: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_repository(request: QueryRequest):
    """Query the indexed repository."""
    global repomind

    if not repomind:
        raise HTTPException(status_code=500, detail="Service not initialized")

    if not repomind.is_indexed:
        raise HTTPException(status_code=400, detail="No index available. Please index a repository first.")

    try:
        result = repomind.query(request.question)

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency_ms=result["latency_ms"],
            prompt_tokens=result.get("prompt_tokens"),
            completion_tokens=result.get("completion_tokens"),
            total_tokens=result.get("total_tokens"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query: {str(e)}")
