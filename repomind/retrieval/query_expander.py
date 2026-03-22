from typing import List
from openai import OpenAI


QUERY_EXPANDER_PROMPT = """你是一个查询扩展助手。给定一个关于代码仓库的问题，请生成 2-3 个语义相似的查询变体，以提高检索的召回率。

请只返回查询变体，每行一个，不要其他解释。

原始问题: {query}
"""


class QueryExpander:
    """Expand user queries using LLM to improve recall."""

    def __init__(self, api_key: str, base_url: str, model: str = "qwen3.5-plus"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def expand(self, query: str, num_variants: int = 3) -> List[str]:
        """
        Expand a query into multiple variants.

        Args:
            query: Original query.
            num_variants: Number of variants to generate.

        Returns:
            List of query variants, including the original query.
        """
        prompt = QUERY_EXPANDER_PROMPT.format(query=query)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
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
            if line and not line.startswith("原始问题"):
                line = line.lstrip("0123456789. -•")
                if line:
                    variants.append(line.strip())
        return variants
