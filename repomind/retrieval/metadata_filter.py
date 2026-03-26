from typing import List, Tuple
from repomind.ingestion.models import CodeChunk


class MetadataFilter:
    """Filter chunks based on metadata."""

    def __init__(self):
        pass

    def filter(
        self,
        chunks_with_scores: List[Tuple[CodeChunk, float]],
        query: str
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Filter chunks based on metadata and query.

        Args:
            chunks_with_scores: List of (chunk, score) tuples.
            query: Original user query.

        Returns:
            Filtered list of (chunk, score) tuples.
        """
        if not chunks_with_scores:
            return []

        filtered = []
        query_lower = query.lower()

        for chunk, score in chunks_with_scores:
            if self._passes_filters(chunk, query_lower):
                filtered.append((chunk, score))

        return filtered if filtered else chunks_with_scores

    def _passes_filters(self, chunk: CodeChunk, query_lower: str) -> bool:
        """Check if a chunk passes the filters."""
        if not self._extension_filter(chunk):
            return False

        return True

    def _extension_filter(self, chunk: CodeChunk) -> bool:
        """Filter by file extension - prefer code files."""
        preferred_extensions = {
            ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp",
            ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
            ".sh", ".bash", ".md", ".txt", ".json", ".yaml", ".yml"
        }
        if "." not in chunk.file_path:
            return True

        ext = chunk.file_path[chunk.file_path.rfind("."):].lower()
        return ext in preferred_extensions
