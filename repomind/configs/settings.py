from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # LLM Configuration
    qwen_api_key: str
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_model: str = "qwen3.5-plus"  # 强 LLM（用于答案生成）
    llm_model_fast: str = "qwen-flash"  # 快 LLM（用于查询扩展等）
    embedding_model: str = "text-embedding-v4"

    # Vector Store Configuration
    vector_store_path: str = "./data/faiss_index"

    # Retrieval Configuration
    retrieval_top_k: int = 20
    retrieval_final_k: int = 5
    rerank_alpha: float = 0.85  # Weight for embedding score (increased for better accuracy)
    rerank_beta: float = 0.15   # Weight for keyword overlap (decreased, just a bonus)
    rerank_lambda: float = 0.75  # MMR relevance-diversity tradeoff (future use)
    rerank_doc_bias: float = 0.05  # Minor boost for document chunks
    rerank_min_doc_count: int = 1  # Minimum doc chunks in final selection
    rerank_min_code_count: int = 1  # Minimum code chunks in final selection

    # Query Expansion Configuration
    enable_query_expansion: bool = True
    query_expansion_variants: int = 2  # Number of variants to generate (original + N)

    # Query Classification Configuration
    enable_query_classification: bool = True  # Enable/disable question complexity classification

    # Generation Configuration
    max_context_tokens: int = 4000

    model_config = {
        "env_prefix": "",
        "env_file": ".env",
        "extra": "ignore",
    }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
