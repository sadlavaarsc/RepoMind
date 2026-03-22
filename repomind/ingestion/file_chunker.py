import os
from typing import List
from repomind.ingestion.models import CodeChunk


class FileChunker:
    """Simple file-level chunker - entire file as one chunk."""

    def __init__(self):
        pass

    def chunk_repository(self, repo_path: str) -> List[CodeChunk]:
        """Chunk an entire repository, each file as a single chunk."""
        chunks = []
        repo_path = os.path.abspath(repo_path)

        if not os.path.isdir(repo_path):
            return chunks

        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_chunk = self.chunk_file(file_path)
                if file_chunk:
                    chunks.append(file_chunk)

        return chunks

    def chunk_file(self, file_path: str) -> CodeChunk:
        """Chunk a single file as one chunk."""
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return None

        language = self._guess_language(file_path)
        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language=language
        )

    def _guess_language(self, file_path: str) -> str:
        """Guess programming language from file extension."""
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".sh": "shell",
            ".md": "markdown",
            ".txt": "text",
        }
        ext = os.path.splitext(file_path)[1].lower()
        return ext_map.get(ext, "unknown")
