import os
from typing import List, Optional
from pathlib import Path
from repomind.ingestion.models import CodeChunk
from repomind.ingestion.parsers.python_parser import PythonParser


class Chunker:
    """Orchestrate code chunking for multiple languages."""

    def __init__(self):
        self.parsers = {
            ".py": PythonParser(),
        }

    def chunk_repository(self, repo_path: str) -> List[CodeChunk]:
        """Chunk an entire repository into code chunks."""
        chunks = []
        repo_path = os.path.abspath(repo_path)

        if not os.path.isdir(repo_path):
            return chunks

        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_chunks = self.chunk_file(file_path)
                chunks.extend(file_chunks)

        return chunks

    def chunk_file(self, file_path: str) -> List[CodeChunk]:
        """Chunk a single file into code chunks."""
        ext = os.path.splitext(file_path)[1].lower()

        if ext in self.parsers:
            parser = self.parsers[ext]
            return parser.parse_file(file_path)
        else:
            return self._chunk_file_heuristic(file_path)

    def _chunk_file_heuristic(self, file_path: str) -> List[CodeChunk]:
        """Simple heuristic chunking for unsupported languages."""
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return []

        language = self._guess_language(file_path)
        return [CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language=language
        )]

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
