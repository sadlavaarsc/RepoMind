"""
LLM-based answer quality evaluator.

Implements three-step evaluation:
1. Context Sufficiency
2. Answer Correctness
3. Grounding Check
"""

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from repomind.generation.llm_service import LLMService


# Prompt templates
PROMPT_SUFFICIENCY = """You are evaluating whether the retrieved context is sufficient to answer a question.

Question:
{query}

Retrieved Context:
{retrieved_context}

Task:
Determine whether the context contains enough information to answer the question.

Rules:
- You MUST rely ONLY on the provided context.
- You MUST quote exact evidence from the context.
- If any critical information is missing, the answer is NOT sufficient.
- Be conservative.

Scoring:
- 2 = Fully sufficient
- 1 = Partially sufficient
- 0 = Not sufficient

Output JSON ONLY, no other text:
{{
  "score": 0|1|2,
  "reason": "...",
  "evidence": ["exact quotes from context"]
}}
"""

PROMPT_CORRECTNESS = """You are evaluating the correctness of an answer.

Question:
{query}

Ground Truth Answer:
{gold_answer}

Model Answer:
{pred_answer}

Task:
Evaluate correctness and completeness.

Rules:
- Minor wording differences are acceptable
- Missing key steps = not fully correct

Scoring:
- 2 = Correct and complete
- 1 = Partially correct
- 0 = Incorrect

Output JSON ONLY, no other text:
{{
  "score": 0|1|2,
  "reason": "..."
}}
"""

PROMPT_GROUNDING = """You are checking whether the answer is supported by the context.

Answer:
{pred_answer}

Context:
{retrieved_context}

Task:
Check whether all claims in the answer are supported by the context.

Rules:
- Every claim must be backed by the context
- If any claim is unsupported, it is not fully grounded

Scoring:
- 2 = Fully grounded
- 1 = Partially grounded
- 0 = Not grounded

Output JSON ONLY, no other text:
{{
  "score": 0|1|2,
  "unsupported_claims": ["..."]
}}
"""


class LLMEvaluator:
    """LLM-based answer quality evaluator."""

    def __init__(
        self,
        model: str = "qwen-flash",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.model = model
        self.api_key = api_key or os.environ.get("QWEN_API_KEY")
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"

        self.llm_service = LLMService(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model
        )

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from LLM output."""
        # Try to find JSON in the text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        # Try to parse directly
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        return None

    async def _evaluate_with_retry(
        self,
        prompt: str,
        max_retries: int = 2
    ) -> Optional[Dict[str, Any]]:
        """Evaluate with retries for JSON parsing."""
        for attempt in range(max_retries + 1):
            try:
                result = self.llm_service.generate(
                    prompt=prompt,
                    temperature=0.3,
                    max_tokens=1000
                )
                content = result["content"]
                parsed = self._extract_json(content)
                if parsed:
                    return parsed
            except Exception as e:
                print(f"  Attempt {attempt + 1} failed: {e}")

        return None

    async def evaluate_single_query(
        self,
        query: str,
        retrieved_context: str,
        pred_answer: str,
        gold_answer: str
    ) -> Dict[str, Any]:
        """
        Evaluate a single query with three steps:
        1. Context Sufficiency
        2. Answer Correctness
        3. Grounding Check
        """
        print(f"Evaluating query: {query[:50]}...")

        # Step 1: Context Sufficiency (only uses query + context)
        print("  Step 1: Context Sufficiency...")
        sufficiency_prompt = PROMPT_SUFFICIENCY.format(
            query=query,
            retrieved_context=retrieved_context
        )
        sufficiency = await self._evaluate_with_retry(sufficiency_prompt) or {
            "score": 0,
            "reason": "Evaluation failed",
            "evidence": []
        }

        # Step 2: Answer Correctness
        print("  Step 2: Answer Correctness...")
        correctness_prompt = PROMPT_CORRECTNESS.format(
            query=query,
            gold_answer=gold_answer,
            pred_answer=pred_answer
        )
        correctness = await self._evaluate_with_retry(correctness_prompt) or {
            "score": 0,
            "reason": "Evaluation failed"
        }

        # Step 3: Grounding Check
        print("  Step 3: Grounding Check...")
        grounding_prompt = PROMPT_GROUNDING.format(
            pred_answer=pred_answer,
            retrieved_context=retrieved_context
        )
        grounding = await self._evaluate_with_retry(grounding_prompt) or {
            "score": 0,
            "unsupported_claims": []
        }

        return {
            "sufficiency": sufficiency,
            "correctness": correctness,
            "grounding": grounding
        }

    async def evaluate_system(
        self,
        repo_name: str,
        system_name: str,
        test_suite_dir: Path,
        results_archive_dir: Path
    ) -> Dict[str, Any]:
        """Evaluate all queries for a system."""
        from repomind.evaluation.result_parser import (
            parse_comparison_report,
            parse_prompt_file,
            find_prompt_file
        )

        # Load test suite
        test_suite_path = test_suite_dir / repo_name / "test_questions.json"
        with open(test_suite_path, "r", encoding="utf-8") as f:
            test_suite = json.load(f)

        # Create question lookup
        question_lookup = {q["id"]: q for q in test_suite["questions"]}

        # Load comparison report
        report_path = results_archive_dir / f"baseline_results_{repo_name}_{system_name}" / "comparison_report.md"
        comparison_data = parse_comparison_report(report_path)

        # Load prompts dir
        prompts_dir = results_archive_dir / f"baseline_results_{repo_name}_{system_name}" / "prompts"

        # Evaluate each query
        query_evals = {}
        for query_id, comparison in comparison_data.items():
            if query_id not in question_lookup:
                continue

            question_data = question_lookup[query_id]
            gold_answer = question_data.get("reference_answer", "")

            # Get retrieved context from prompt file
            prompt_file = find_prompt_file(prompts_dir, query_id)
            retrieved_context = ""
            if prompt_file:
                _, retrieved_context = parse_prompt_file(prompt_file)

            # Evaluate
            eval_result = await self.evaluate_single_query(
                query=comparison["question"],
                retrieved_context=retrieved_context,
                pred_answer=comparison["pred_answer"],
                gold_answer=gold_answer
            )

            query_evals[query_id] = {
                **comparison,
                "gold_answer": gold_answer,
                "evaluation": eval_result
            }

        return {
            "repo": repo_name,
            "system": system_name,
            "query_evals": query_evals
        }
