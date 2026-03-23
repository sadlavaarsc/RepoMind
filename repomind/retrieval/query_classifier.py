from typing import Literal
from openai import OpenAI


QUERY_CLASSIFIER_PROMPT = """判断这个问题是简单问题还是复杂问题。

简单问题：问"是什么"、"找文件"、"变量名/函数名"、"列举清单"
复杂问题：问"为什么"、"如何实现"、"业务逻辑"、"项目做什么"、"详细解释"

只回答 "simple" 或 "complex"，不要其他内容。

问题：{query}
"""


class QueryClassifier:
    """Classify queries as simple or complex using fast LLM."""

    def __init__(self, api_key: str, base_url: str, model: str = "qwen-flash"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def classify(self, query: str) -> Literal["simple", "complex"]:
        """
        Classify a query as simple or complex.

        Args:
            query: User query.

        Returns:
            "simple" or "complex".
        """
        prompt = QUERY_CLASSIFIER_PROMPT.format(query=query)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # 极低温度，确保输出稳定
                max_tokens=10  # 限制输出非常短
            )
            content = response.choices[0].message.content.strip().lower()

            if "simple" in content:
                return "simple"
            elif "complex" in content:
                return "complex"
            else:
                # 默认返回 complex，保守策略
                return "complex"
        except Exception:
            # 出错时默认返回 complex
            return "complex"
