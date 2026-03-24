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

    # New fields for multi-level chunking
    chunk_type: Optional[str] = Field(None, description="Type of chunk: file | class | function | block")
    name: Optional[str] = Field(None, description="Name of this chunk (file name, class name, function name, etc.)")
    signature: Optional[str] = Field(None, description="Function or method signature")
    docstring: Optional[str] = Field(None, description="Docstring of the function/class/module")
    summary: Optional[str] = Field(None, description="LLM-generated summary of this chunk")
    structured_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Compressed structured data for this chunk")

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

    def get_embedding_text(self) -> str:
        """
        Get the text to use for embedding.
        Priority: summary > structure > code
        """
        parts = []

        if self.chunk_type:
            parts.append(f"[TYPE] {self.chunk_type}")
        if self.name:
            parts.append(f"Name: {self.name}")
        parts.append(f"File: {self.file_path}")

        if self.summary:
            parts.append("")
            parts.append("Summary:")
            parts.append(self.summary)

        if self.structured_data and "calls" in self.structured_data:
            parts.append("")
            parts.append("Calls:")
            parts.append(", ".join(self.structured_data["calls"]))

        parts.append("")
        parts.append("Code:")
        parts.append(self.content)

        return "\n".join(parts)
