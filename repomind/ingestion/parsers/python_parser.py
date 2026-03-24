import ast
import os
from typing import List, Optional
from repomind.ingestion.models import CodeChunk
from repomind.ingestion.parsers.python_ast_extractor import PythonASTExtractor


class PythonParser:
    """Parse Python files using AST to extract multi-level chunks."""

    def __init__(self):
        self.language = "python"
        self.extractor = PythonASTExtractor()

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

        lines = content.splitlines()
        chunks = []

        # Extract all chunk types
        self._extract_multi_level_chunks(tree, file_path, content, lines, chunks)

        # If no chunks extracted (pure script file), try to extract script blocks
        if not chunks:
            self._extract_script_chunks(tree, file_path, content, lines, chunks)

        # If still no chunks, fall back to file-level
        if not chunks:
            chunks.append(self._create_file_level_chunk(file_path, content))

        return chunks

    def _set_parents(self, tree: ast.AST) -> None:
        """Set parent pointers for all nodes in the AST."""
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

    def _extract_multi_level_chunks(
        self,
        tree: ast.AST,
        file_path: str,
        full_content: str,
        lines: List[str],
        chunks: List[CodeChunk]
    ) -> None:
        """Extract multi-level chunks: file, class, function."""
        self._set_parents(tree)

        # 1. File-level chunk (module docstring + constants)
        file_chunk = self._create_file_chunk(tree, file_path, full_content, lines)
        if file_chunk:
            chunks.append(file_chunk)

        # 2. Traverse AST for classes and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Class-level chunk
                class_chunk = self._create_class_chunk(node, file_path, lines)
                if class_chunk:
                    chunks.append(class_chunk)

                # Methods within class
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        func_chunk = self._create_function_chunk(
                            item, file_path, lines, class_name=node.name
                        )
                        if func_chunk:
                            chunks.append(func_chunk)

            elif isinstance(node, ast.FunctionDef) and self._is_top_level(node):
                # Top-level function
                func_chunk = self._create_function_chunk(
                    node, file_path, lines, class_name=None
                )
                if func_chunk:
                    chunks.append(func_chunk)

    def _extract_script_chunks(
        self,
        tree: ast.AST,
        file_path: str,
        full_content: str,
        lines: List[str],
        chunks: List[CodeChunk]
    ) -> None:
        """Extract chunks from pure script files (no functions/classes)."""
        # Extract file-level chunk first
        file_chunk = self._create_file_chunk(tree, file_path, full_content, lines)
        if file_chunk:
            chunks.append(file_chunk)

        # Extract script blocks
        script_blocks = self.extractor.extract_script_blocks(tree, full_content, lines)

        for block in script_blocks:
            start_line = block["start_line"]
            end_line = min(block["end_line"] + 1, len(lines))
            content = "\n".join(lines[start_line:end_line])

            if content.strip():
                chunk = CodeChunk(
                    content=content,
                    file_path=file_path,
                    function_name=None,
                    class_name=None,
                    language=self.language,
                    chunk_type="block",
                    name=f"script_block_{start_line}",
                    structured_data=block
                )
                chunks.append(chunk)

    def _is_top_level(self, node: ast.AST) -> bool:
        """Check if a node is at top level (not inside a class)."""
        parent = getattr(node, "parent", None)
        return parent is None or not isinstance(parent, ast.ClassDef)

    def _create_file_chunk(
        self,
        tree: ast.AST,
        file_path: str,
        full_content: str,
        lines: List[str]
    ) -> Optional[CodeChunk]:
        """Create a file-level chunk with module info."""
        file_info = self.extractor.extract_file_info(tree, full_content)

        # Include module docstring and top-level constants
        start_line = 0
        # Find where the actual code starts (after docstring)
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('"') and not line.strip().startswith("#"):
                start_line = i
                break

        # Include up to first function/class or first 50 lines
        end_line = len(lines)
        for i, node in enumerate(tree.body):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                end_line = node.lineno - 1
                break

        end_line = min(end_line, start_line + 100, len(lines))
        content = "\n".join(lines[start_line:end_line])

        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language=self.language,
            chunk_type="file",
            name=os.path.basename(file_path),
            docstring=file_info.get("docstring"),
            structured_data=file_info
        )

    def _create_class_chunk(
        self,
        node: ast.ClassDef,
        file_path: str,
        lines: List[str]
    ) -> Optional[CodeChunk]:
        """Create a class-level chunk."""
        class_info = self.extractor.extract_class_info(node)

        start_line = node.lineno - 1
        # Find end of class definition (up to first method)
        end_line = len(lines)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                end_line = item.lineno - 1
                break

        end_line = min(end_line, getattr(node, "end_lineno", len(lines)))
        content = "\n".join(lines[start_line:end_line])

        if not content.strip():
            return None

        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=node.name,
            language=self.language,
            chunk_type="class",
            name=node.name,
            docstring=class_info.get("docstring"),
            structured_data=class_info
        )

    def _create_function_chunk(
        self,
        node: ast.FunctionDef,
        file_path: str,
        lines: List[str],
        class_name: Optional[str]
    ) -> Optional[CodeChunk]:
        """Create a CodeChunk from a function definition."""
        func_info = self.extractor.extract_function_info(node)

        start_line = node.lineno - 1
        end_line = getattr(node, "end_lineno", len(lines))
        content = "\n".join(lines[start_line:end_line])

        if not content.strip():
            return None

        name = node.name
        if class_name:
            name = f"{class_name}.{node.name}"

        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=node.name,
            class_name=class_name,
            language=self.language,
            chunk_type="function",
            name=name,
            signature=func_info.get("signature"),
            docstring=func_info.get("docstring"),
            structured_data=func_info
        )

    def _create_file_level_chunk(self, file_path: str, content: str) -> CodeChunk:
        """Create a file-level chunk when AST parsing fails."""
        return CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language=self.language,
            chunk_type="file",
            name=os.path.basename(file_path)
        )
