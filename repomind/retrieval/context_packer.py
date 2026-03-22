from typing import List, Tuple, Set
import tiktoken
from repomind.ingestion.models import CodeChunk


class ContextPacker:
    """Pack retrieved chunks into context, with deduplication and token limit."""

    def __init__(self, max_tokens: int = 4000, encoding_name: str = "cl100k_base"):
        self.max_tokens = max_tokens
        self.encoding = tiktoken.get_encoding(encoding_name)

    def pack(
        self,
        chunks_with_scores: List[Tuple[CodeChunk, float]],
        final_k: int = 5
    ) -> List[CodeChunk]:
        """
        Pack chunks into context.

        Args:
            chunks_with_scores: List of (chunk, score) tuples.
            final_k: Maximum number of chunks to include.

        Returns:
            List of packed code chunks.
        """
        if not chunks_with_scores:
            return []

        deduplicated = self._deduplicate(chunks_with_scores)

        limited = deduplicated[:final_k]

        packed = self._trim_to_token_limit([chunk for chunk, _ in limited])

        return packed

    def _deduplicate(
        self,
        chunks_with_scores: List[Tuple[CodeChunk, float]]
    ) -> List[Tuple[CodeChunk, float]]:
        """Remove duplicate chunks."""
        seen: Set[str] = set()
        result = []

        for chunk, score in chunks_with_scores:
            identifier = chunk.get_identifier()
            if identifier not in seen:
                seen.add(identifier)
                result.append((chunk, score))

        return result

    def _trim_to_token_limit(self, chunks: List[CodeChunk]) -> List[CodeChunk]:
        """Trim chunks to stay under token limit."""
        result = []
        total_tokens = 0

        for chunk in chunks:
            chunk_tokens = self._count_tokens(chunk)
            if total_tokens + chunk_tokens <= self.max_tokens:
                result.append(chunk)
                total_tokens += chunk_tokens
            else:
                continue

        return result if result else chunks[:1]

    def _count_tokens(self, chunk: CodeChunk) -> int:
        """Count tokens in a chunk."""
        text = self._format_chunk(chunk)
        return len(self.encoding.encode(text))

    def _format_chunk(self, chunk: CodeChunk) -> str:
        """Format a chunk for context."""
        header = f"File: {chunk.file_path}"
        if chunk.class_name:
            header += f" | Class: {chunk.class_name}"
        if chunk.function_name:
            header += f" | Function: {chunk.function_name}"
        return f"--- {header} ---\n{chunk.content}\n"
