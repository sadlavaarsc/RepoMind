from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class IndexRequest(BaseModel):
    """Request schema for POST /index."""
    repo_path: str = Field(..., description="Path to the repository to index")


class IndexResponse(BaseModel):
    """Response schema for POST /index."""
    success: bool
    message: str
    num_chunks: Optional[int] = None
    index_path: Optional[str] = None


class QueryRequest(BaseModel):
    """Request schema for POST /query."""
    question: str = Field(..., description="Question to ask about the repository")


class QueryResponse(BaseModel):
    """Response schema for POST /query."""
    answer: str
    sources: List[str]
    latency_ms: Optional[float] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str
    version: str
