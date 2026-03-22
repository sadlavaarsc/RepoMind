from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CodeChunk(BaseModel):
    """Represents a chunk of code with metadata."""

    content: str = Field(..., description="The code content of the chunk")
    file_path: str = Field(..., description="Path to the source file")
    function_name: Optional[str] = Field(None, description="Name of the function, if applicable")
    class_name: Optional[str] = Field(None, description="Name of the class, if applicable")
    language: str = Field(..., description="Programming language of the code")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata (reserved for future use)")

    def get_identifier(self) -> str:
        """Get a unique identifier for this chunk."""
        parts = [self.file_path]
        if self.class_name:
            parts.append(self.class_name)
        if self.function_name:
            parts.append(self.function_name)
        return "::".join(parts)

    def summarize_chunk(self) -> Optional[str]:
        """Placeholder for future LLM-based summarization."""
        return None
