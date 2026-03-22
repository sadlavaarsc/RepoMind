import ast
import os
from typing import List, Optional
from repomind.ingestion.models import CodeChunk


class PythonParser:
    """Parse Python files using AST to extract function-level chunks."""

    def __init__(self):
        self.language = "python"

    def parse_file(self, file_path: str) -> List[CodeChunk]:
        """Parse a Python file and return code chunks."""
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return []

        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError:
            return [self._create_file_level_chunk(file_path, content)]

        chunks = []
        self._extract_chunks(tree, file_path, content, chunks)

        if not chunks:
            chunks.append(self._create_file_level_chunk(file_path, content))

        return chunks

    def _extract_chunks(
        self,
        tree: ast.AST,
        file_path: str,
        full_content: str,
        chunks: List[CodeChunk]
    ) -> None:
        """Extract chunks from the AST."""
        lines = full_content.splitlines()

        # Extract top-level functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and self._is_top_level(node):
                chunk = self._create_function_chunk(
                    node, file_path, lines, class_name=None
                )
                if chunk:
                    chunks.append(chunk)

            # Extract methods within classes
            elif isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        chunk = self._create_function_chunk(
                            item, file_path, lines, class_name=node.name
                        )
                        if chunk:
                            chunks.append(chunk)

    def _is_top_level(self, node: ast.AST) -> bool:
        """Check if a node is at top level (not inside a class)."""
        return not hasattr(node, "parent") or not isinstance(node.parent, ast.ClassDef)

    def _create_function_chunk(
        self,
        node: ast.FunctionDef,
        file_path: str,
        lines: List[str],
        class_name: Optional[str]
    ) -> Optional[CodeChunk]:
        """Create a CodeChunk from a function definition."""
        start_line = node.lineno - 1
        end_line = getattr(node, "end_lineno", len(lines))
        content = "\n".join(lines[start_line:end_line])

        if not content.strip():
            return None

        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=node.name,
            class_name=class_name,
            language=self.language
        )

    def _create_file_level_chunk(self, file_path: str, content: str) -> CodeChunk:
        """Create a file-level chunk when AST parsing fails."""
        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language=self.language
        )
