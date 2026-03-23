import os
import time
from typing import Dict, Any
from pathlib import Path
from repomind.generation.llm_service import LLMService
from repomind.configs.settings import get_settings


LLM_ONLY_PROMPT = """你是一个代码仓库理解助手。

你将看到一个代码仓库的完整内容。请基于这些代码回答用户的问题。

请给出简洁明了的答案，并在适当时引用相关的文件路径。

代码仓库内容：
{repository_content}

用户问题：{query}
"""


class LLMOnly:
    """LLM-only baseline: no retrieval, direct prompting."""

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.repository_content = ""

    def load_repository(self, repo_path: str) -> None:
        """Load repository content into memory."""
        repo_path = Path(repo_path)
        if not repo_path.is_dir():
            return

        content_parts = []

        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and self._should_include_file(file_path):
                try:
                    relative_path = file_path.relative_to(repo_path)
                    file_content = file_path.read_text(encoding="utf-8")
                    content_parts.append(f"# File: {relative_path}\n{file_content}\n")
                except Exception:
                    continue

        self.repository_content = "\n".join(content_parts)

    def query(self, query: str) -> Dict[str, Any]:
        """Query using LLM-only approach."""
        start_time = time.time()

        system_prompt = "你是一个代码仓库理解助手。"
        prompt = LLM_ONLY_PROMPT.format(
            repository_content=self.repository_content[:8000],
            query=query
        )

        result = self.llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2000
        )

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        return {
            "answer": result["content"],
            "sources": [],
            "latency_ms": latency_ms,
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "total_tokens": result["total_tokens"],
            "full_prompt": {
                "system_prompt": system_prompt,
                "user_prompt": prompt
            }
        }

    def _should_include_file(self, file_path: Path) -> bool:
        """Check if a file should be included in the context."""
        include_extensions = {
            ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp",
            ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".sh", ".md", ".txt"
        }
        return file_path.suffix.lower() in include_extensions
