import ast
from typing import List, Dict, Any, Optional, Set, Tuple


class PythonASTExtractor:
    """
    Extract structured information from Python AST.
    Focuses on compressed representations, NOT full code.
    """

    def __init__(self):
        pass

    def _set_parents(self, tree: ast.AST) -> None:
        """Set parent pointers for all nodes in the AST."""
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

    def extract_file_info(self, tree: ast.AST, content: str) -> Dict[str, Any]:
        """
        Extract file-level structured information.
        Returns compressed data only, no full code.
        """
        self._set_parents(tree)

        imports = []
        top_level_symbols = []
        module_docstring = ast.get_docstring(tree)

        # Extract imports and top-level symbols
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.extend(self._extract_imports(node))
            elif isinstance(node, ast.FunctionDef):
                top_level_symbols.append(node.name)
            elif isinstance(node, ast.ClassDef):
                top_level_symbols.append(node.name)
            elif isinstance(node, ast.Assign):
                # Extract top-level constants
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        top_level_symbols.append(target.id)

        return {
            "type": "file",
            "imports": imports,
            "symbols": top_level_symbols,
            "docstring": module_docstring
        }

    def extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """
        Extract class-level structured information.
        Returns compressed data only, no full method bodies.
        """
        class_docstring = ast.get_docstring(node)
        methods = []
        attributes = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._get_function_signature(item))
            elif isinstance(item, ast.Assign):
                # Extract class attributes
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)

        return {
            "type": "class",
            "class_name": node.name,
            "methods": methods,
            "attributes": attributes,
            "docstring": class_docstring
        }

    def extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extract function-level structured information.
        Returns compressed data only, no full function body.
        """
        func_docstring = ast.get_docstring(node)
        signature = self._get_function_signature(node)
        called_functions = self._extract_called_functions(node)

        return {
            "type": "function",
            "name": node.name,
            "signature": signature,
            "docstring": func_docstring,
            "calls": list(called_functions)
        }

    def _extract_imports(self, node: ast.AST) -> List[str]:
        """Extract import statements as strings."""
        imports = []
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for name in node.names:
                if module:
                    imports.append(f"{module}.{name.name}")
                else:
                    imports.append(name.name)
        return imports

    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Get the function signature as a string."""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)

        # Handle *args
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")

        # Handle **kwargs
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")

        return f"{node.name}({', '.join(args)})"

    def _extract_called_functions(self, node: ast.FunctionDef) -> Set[str]:
        """Extract function calls within a function body."""
        calls = set()

        class CallVisitor(ast.NodeVisitor):
            def __init__(self):
                self.calls = set()

            def visit_Call(self, call_node):
                if isinstance(call_node.func, ast.Name):
                    self.calls.add(call_node.func.id)
                elif isinstance(call_node.func, ast.Attribute):
                    # Get the method name
                    self.calls.add(call_node.func.attr)
                self.generic_visit(call_node)

        visitor = CallVisitor()
        visitor.visit(node)
        return visitor.calls

    def extract_script_blocks(self, tree: ast.AST, content: str, lines: List[str]) -> List[Dict[str, Any]]:
        """
        Extract top-level script code blocks for files without many functions/classes.
        Returns compressed block information.
        """
        blocks = []
        current_block_start = None
        current_block_comments = []

        for i, node in enumerate(tree.body):
            # Skip imports and function/class definitions
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
                if current_block_start is not None:
                    # End of a script block
                    block_end = node.lineno - 2 if node.lineno else len(lines)
                    if block_end >= current_block_start:
                        blocks.append({
                            "type": "block",
                            "start_line": current_block_start,
                            "end_line": block_end,
                            "comments": current_block_comments.copy()
                        })
                    current_block_start = None
                    current_block_comments = []
                continue

            # This is a top-level statement - start or continue a block
            if current_block_start is None:
                current_block_start = node.lineno - 1 if node.lineno else 0

        # Add the last block if any
        if current_block_start is not None:
            blocks.append({
                "type": "block",
                "start_line": current_block_start,
                "end_line": len(lines) - 1,
                "comments": current_block_comments
            })

        return blocks
