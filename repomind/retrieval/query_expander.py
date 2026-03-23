from typing import List
from openai import OpenAI


# 简化的提示词，专门为 fast LLM 设计
QUERY_EXPANDER_PROMPT = """生成{num_variants}个相似查询，每行一个，不要其他内容。
原始问题: {query}
"""


class QueryExpander:
    """Expand user queries using LLM to improve recall."""

    def __init__(self, api_key: str, base_url: str, model: str = "qwen3.5-plus"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def expand(self, query: str, num_variants: int = 2) -> List[str]:
        """
        Expand a query into multiple variants.

        Args:
            query: Original query.
            num_variants: Number of variants to generate.

        Returns:
            List of query variants, including the original query.
        """
        prompt = QUERY_EXPANDER_PROMPT.format(query=query, num_variants=num_variants)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # 降低温度，提高输出确定性
                max_tokens=200  # 限制输出长度
            )
            content = response.choices[0].message.content
            variants = self._parse_response(content)
        except Exception:
            variants = []

        result = [query] + variants
        return result[:num_variants + 1]

    def _parse_response(self, content: str) -> List[str]:
        """Parse LLM response into query variants."""
        variants = []
        for line in content.splitlines():
            line = line.strip()
            if line and len(line) > 3:  # 过滤掉太短的行
                line = line.lstrip("0123456789. -•*")
                if line and len(line) > 3:
                    variants.append(line.strip())
        return variants
