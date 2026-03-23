from typing import List, Dict, Any, Optional
from repomind.ingestion.models import CodeChunk
from repomind.generation.llm_service import LLMService


SYSTEM_PROMPT = """你是一个代码仓库理解助手。请基于提供的代码上下文来回答问题。

回答要求：
1. 尽可能引用相关的文件路径
2. 如果找到相关的函数或类，请提及它们的名称
3. 如果上下文中没有足够的信息，请诚实说明
4. 保持回答简洁明了

回答格式：
```
[你的回答]

参考文件：
- [文件路径1]
- [文件路径2]
...
```
"""


ANSWER_PROMPT = """请基于以下代码上下文回答问题。

问题：{query}

代码上下文：
{context}

请给出你的答案。
"""


class AnswerGenerator:
    """Generate answers using retrieved code chunks."""

    def __init__(
        self,
        llm_service: LLMService,
        llm_service_fast: Optional[LLMService] = None
    ):
        self.llm_service = llm_service  # strong LLM (qwen3.5-plus)
        self.llm_service_fast = llm_service_fast  # fast LLM (qwen-flash)

    def generate(
        self,
        query: str,
        chunks: List[CodeChunk],
        use_fast_model: bool = False
    ) -> Dict[str, Any]:
        """
        Generate an answer from query and retrieved chunks.

        Args:
            query: User question.
            chunks: Retrieved code chunks.
            use_fast_model: Whether to use the fast LLM instead of strong LLM.

        Returns:
            Dictionary with "answer", "sources", token usage, and full prompt.
        """
        if not chunks:
            return {
                "answer": "没有找到相关的代码上下文来回答这个问题。",
                "sources": [],
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "full_prompt": None,
                "model_used": "none",
            }

        context = self._format_context(chunks)
        prompt = ANSWER_PROMPT.format(query=query, context=context)

        # 选择使用的 LLM
        if use_fast_model and self.llm_service_fast is not None:
            service = self.llm_service_fast
            model_used = "fast"
        else:
            service = self.llm_service
            model_used = "strong"

        result = service.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=2000
        )

        sources = list({chunk.file_path for chunk in chunks})

        return {
            "answer": result["content"],
            "sources": sources,
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "total_tokens": result["total_tokens"],
            "full_prompt": {
                "system_prompt": SYSTEM_PROMPT,
                "user_prompt": prompt
            },
            "model_used": model_used,
        }

    def _format_context(self, chunks: List[CodeChunk]) -> str:
        """Format code chunks into context string."""
        parts = []
        for i, chunk in enumerate(chunks, 1):
            header = f"--- 代码片段 {i} ---\n"
            header += f"文件: {chunk.file_path}\n"
            if chunk.class_name:
                header += f"类: {chunk.class_name}\n"
            if chunk.function_name:
                header += f"函数: {chunk.function_name}\n"
            header += "---\n"
            parts.append(header + chunk.content)
        return "\n\n".join(parts)
