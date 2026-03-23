"""
Hallucination detector for RAG system answers.

Detects hallucinations by checking if mentioned entities exist in the codebase.
"""

import re
from typing import List, Set, Dict, Any, Optional
from pathlib import Path
import ast


class CodeEntityIndex:
    """Index of entities in a codebase for hallucination detection."""

    def __init__(self):
        self.files: Set[str] = set()
        self.functions: Set[str] = set()
        self.classes: Set[str] = set()
        self.variables: Set[str] = set()

    def build_from_repository(self, repo_path: str) -> None:
        """
        Build entity index from a repository.

        Args:
            repo_path: Path to the repository
        """
        repo_path = Path(repo_path)

        for py_file in repo_path.rglob("*.py"):
            self._index_file(py_file)

    def _index_file(self, file_path: Path) -> None:
        """Index a single Python file."""
        try:
            # Add file to index (relative path)
            rel_path = str(file_path.relative_to(file_path.parent.parent.parent))
            self.files.add(rel_path)
            self.files.add(file_path.name)

            # Parse AST for functions, classes, variables
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.functions.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    self.classes.add(node.name)
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    self.variables.add(node.id)

        except Exception:
            pass


class HallucinationDetector:
    """Detects hallucinations in LLM answers by checking entity existence."""

    # Patterns to extract entities from answers
    FILE_PATTERNS = [
        r'["\']([a-zA-Z0-9_\-./]+\.py)["\']',
        r'["\']([a-zA-Z0-9_\-/]+/[a-zA-Z0-9_\-./]+)["\']',
        r'文件[：:]\s*([a-zA-Z0-9_\-./]+\.py)',
        r'参考[文件]*[：:]\s*([a-zA-Z0-9_\-./]+\.py)',
    ]

    FUNCTION_PATTERNS = [
        r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
        r'函数[：:]\s*([a-zA-Z_][a-zA-Z0-9_]*)',
        r'`([a-zA-Z_][a-zA-Z0-9_]*)\([^)]*\)`',
    ]

    CLASS_PATTERNS = [
        r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'类[：:]\s*([a-zA-Z_][a-zA-Z0-9_]*)',
    ]

    def __init__(self, entity_index: CodeEntityIndex):
        """
        Initialize hallucination detector.

        Args:
            entity_index: CodeEntityIndex with known entities
        """
        self.index = entity_index

    def extract_entities(self, answer: str) -> Dict[str, List[str]]:
        """
        Extract entities from an answer.

        Args:
            answer: LLM-generated answer

        Returns:
            Dictionary with 'files', 'functions', 'classes' lists
        """
        entities = {
            "files": [],
            "functions": [],
            "classes": [],
        }

        # Extract files
        for pattern in self.FILE_PATTERNS:
            matches = re.findall(pattern, answer)
            entities["files"].extend(matches)

        # Extract functions
        for pattern in self.FUNCTION_PATTERNS:
            matches = re.findall(pattern, answer)
            # Filter out common words that might look like functions
            functions = [m for m in matches if m not in ["if", "for", "while", "def", "class", "return"]]
            entities["functions"].extend(functions)

        # Extract classes
        for pattern in self.CLASS_PATTERNS:
            matches = re.findall(pattern, answer)
            entities["classes"].extend(matches)

        # Deduplicate
        entities["files"] = list(set(entities["files"]))
        entities["functions"] = list(set(entities["functions"]))
        entities["classes"] = list(set(entities["classes"]))

        return entities

    def detect_hallucinations(self, answer: str) -> Dict[str, Any]:
        """
        Detect hallucinations in an answer.

        Args:
            answer: LLM-generated answer

        Returns:
            Dictionary with:
            - hallucination_rate: float (0.0 to 1.0)
            - total_entities: int
            - hallucinated_entities: int
            - details: dict with hallucinated files/functions/classes
        """
        entities = self.extract_entities(answer)

        hallucinated = {
            "files": [],
            "functions": [],
            "classes": [],
        }

        verified = {
            "files": [],
            "functions": [],
            "classes": [],
        }

        # Check files
        for file_name in entities["files"]:
            if self._is_file_known(file_name):
                verified["files"].append(file_name)
            else:
                hallucinated["files"].append(file_name)

        # Check functions
        for func_name in entities["functions"]:
            if func_name in self.index.functions:
                verified["functions"].append(func_name)
            else:
                hallucinated["functions"].append(func_name)

        # Check classes
        for class_name in entities["classes"]:
            if class_name in self.index.classes:
                verified["classes"].append(class_name)
            else:
                hallucinated["classes"].append(class_name)

        # Calculate rates
        total_files = len(entities["files"])
        total_functions = len(entities["functions"])
        total_classes = len(entities["classes"])
        total_entities = total_files + total_functions + total_classes

        hallucinated_files = len(hallucinated["files"])
        hallucinated_functions = len(hallucinated["functions"])
        hallucinated_classes = len(hallucinated["classes"])
        total_hallucinated = hallucinated_files + hallucinated_functions + hallucinated_classes

        hallucination_rate = total_hallucinated / max(total_entities, 1)

        return {
            "hallucination_rate": hallucination_rate,
            "total_entities": total_entities,
            "hallucinated_entities": total_hallucinated,
            "verified_entities": total_entities - total_hallucinated,
            "details": {
                "hallucinated": hallucinated,
                "verified": verified,
            }
        }

    def _is_file_known(self, file_name: str) -> bool:
        """Check if a file is known (by full path or just name)."""
        if file_name in self.index.files:
            return True
        # Check if the base name matches
        base_name = Path(file_name).name
        if base_name in self.index.files:
            return True
        return False
