import os
import json
from typing import Dict, Any, Optional, List
from openai import OpenAI


class SummaryGenerator:
    """
    Generate LLM summaries for code chunks using fast model.
    IMPORTANT: Only uses compressed structured data as input, NEVER full code.
    """

    # Fast model configuration
    MODEL_ID = "qwen3.5-fast"
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    API_KEY_ENV = "QWEN_API_KEY"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv(self.API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"API key must be provided or set in {self.API_KEY_ENV}")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.BASE_URL
        )

    def generate_function_summary(self, structured_data: Dict[str, Any]) -> Optional[str]:
        """
        Generate a summary for a function using compressed structured data.

        Args:
            structured_data: Compressed function info from PythonASTExtractor

        Returns:
            Summary string, or None if failed
        """
        prompt = self._build_function_summary_prompt(structured_data)

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are a code analysis assistant. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            content = response.choices[0].message.content
            if content:
                # Parse JSON response
                try:
                    result = json.loads(content)
                    return self._format_summary_from_json(result)
                except json.JSONDecodeError:
                    # Fallback: return raw content if JSON parsing fails
                    return content.strip()

        except Exception as e:
            print(f"Warning: Failed to generate function summary: {e}")
            return None

    def generate_class_summary(self, structured_data: Dict[str, Any]) -> Optional[str]:
        """
        Generate a summary for a class using compressed structured data.

        Args:
            structured_data: Compressed class info from PythonASTExtractor

        Returns:
            Summary string, or None if failed
        """
        prompt = self._build_class_summary_prompt(structured_data)

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are a code analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )

            content = response.choices[0].message.content
            if content:
                return content.strip()

        except Exception as e:
            print(f"Warning: Failed to generate class summary: {e}")
            return None

    def generate_file_summary(self, structured_data: Dict[str, Any]) -> Optional[str]:
        """
        Generate a summary for a file using compressed structured data.

        Args:
            structured_data: Compressed file info from PythonASTExtractor

        Returns:
            Summary string, or None if failed
        """
        prompt = self._build_file_summary_prompt(structured_data)

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are a code analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )

            content = response.choices[0].message.content
            if content:
                return content.strip()

        except Exception as e:
            print(f"Warning: Failed to generate file summary: {e}")
            return None

    def _build_function_summary_prompt(self, structured_data: Dict[str, Any]) -> str:
        """Build prompt for function summary using ONLY structured data."""
        return f"""You are analyzing a Python function.
Summarize based on the structured data below.
Do NOT ask for the full code - work with what you have.

Include in your summary:
- purpose of the function
- inputs
- outputs
- side effects (if any)
- dependencies (called functions)

Structured Input:
{json.dumps(structured_data, indent=2)}

Output JSON format:
{{
  "desc": "Brief description of what this function does",
  "inputs": "Description of inputs",
  "outputs": "Description of outputs",
  "calls": ["list", "of", "called", "functions"]
}}

ONLY output valid JSON, no other text."""

    def _build_class_summary_prompt(self, structured_data: Dict[str, Any]) -> str:
        """Build prompt for class summary using ONLY structured data."""
        return f"""You are analyzing a Python class.
Summarize the class responsibility and key behaviors based on the structured data below.

Structured Input:
{json.dumps(structured_data, indent=2)}

Output a concise 2-3 sentence summary of this class."""

    def _build_file_summary_prompt(self, structured_data: Dict[str, Any]) -> str:
        """Build prompt for file summary using ONLY structured data."""
        return f"""You are analyzing a Python module/file.
Summarize the purpose of this file based on the structured data below.

Structured Input:
{json.dumps(structured_data, indent=2)}

Output a concise 1-2 sentence summary of what this module contains and its purpose."""

    def _format_summary_from_json(self, json_result: Dict[str, Any]) -> str:
        """Format the JSON summary result into a readable string."""
        parts = []

        if "desc" in json_result:
            parts.append(json_result["desc"])
        if "inputs" in json_result and json_result["inputs"]:
            parts.append(f"Inputs: {json_result['inputs']}")
        if "outputs" in json_result and json_result["outputs"]:
            parts.append(f"Outputs: {json_result['outputs']}")
        if "calls" in json_result and json_result["calls"]:
            parts.append(f"Calls: {', '.join(json_result['calls'])}")

        return " ".join(parts)

    def batch_generate_summaries(self, chunks: List[Any], max_workers: int = 5) -> List[Any]:
        """
        Generate summaries for a list of chunks in batch.
        Note: This is a placeholder - actual batch processing would need
        to handle API rate limits.
        """
        # For now, process sequentially
        for chunk in chunks:
            if not hasattr(chunk, "structured_data") or not chunk.structured_data:
                continue

            chunk_type = chunk.chunk_type
            summary = None

            if chunk_type == "function":
                summary = self.generate_function_summary(chunk.structured_data)
            elif chunk_type == "class":
                summary = self.generate_class_summary(chunk.structured_data)
            elif chunk_type == "file":
                summary = self.generate_file_summary(chunk.structured_data)

            if summary:
                chunk.summary = summary

        return chunks
