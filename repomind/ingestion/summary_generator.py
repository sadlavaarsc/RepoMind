import os
import json
from typing import Dict, Any, Optional, List, Tuple
from openai import OpenAI


class SummaryGenerator:
    """
    Generate LLM summaries for code chunks using fast model.
    IMPORTANT: Only uses compressed structured data as input, NEVER full code.
    """

    # Fast model configuration
    MODEL_ID = "qwen-flash"
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    API_KEY_ENV = "QWEN_API_KEY"

    def __init__(self, api_key: Optional[str] = None, save_logs: bool = True, log_dir: Optional[str] = None):
        self.api_key = api_key or os.getenv(self.API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"API key must be provided or set in {self.API_KEY_ENV}")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.BASE_URL
        )

        self.save_logs = save_logs
        self.log_dir = log_dir
        if save_logs and log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # Store all generation logs
        self.generation_logs: List[Dict[str, Any]] = []

    def generate_function_summary(self, structured_data: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Generate a summary for a function using compressed structured data.

        Args:
            structured_data: Compressed function info from PythonASTExtractor

        Returns:
            Tuple of (summary string or None, generation_log dict with prompt and output)
        """
        system_prompt = "You are a code analysis assistant. Output only valid JSON."
        user_prompt = self._build_function_summary_prompt(structured_data)

        generation_log = {
            "chunk_type": "function",
            "structured_data": structured_data,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "raw_output": None,
            "summary": None,
            "success": False,
            "error": None
        }

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            content = response.choices[0].message.content
            generation_log["raw_output"] = content

            if content:
                # Parse JSON response
                try:
                    result = json.loads(content)
                    summary = self._format_summary_from_json(result)
                    generation_log["summary"] = summary
                    generation_log["success"] = True
                    self._save_generation_log(generation_log)
                    return summary, generation_log
                except json.JSONDecodeError:
                    # Fallback: return raw content if JSON parsing fails
                    summary = content.strip()
                    generation_log["summary"] = summary
                    generation_log["success"] = True
                    self._save_generation_log(generation_log)
                    return summary, generation_log

        except Exception as e:
            print(f"Warning: Failed to generate function summary: {e}")
            generation_log["error"] = str(e)
            self._save_generation_log(generation_log)
            return None, generation_log

    def generate_class_summary(self, structured_data: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Generate a summary for a class using compressed structured data.

        Args:
            structured_data: Compressed class info from PythonASTExtractor

        Returns:
            Tuple of (summary string or None, generation_log dict with prompt and output)
        """
        system_prompt = "You are a code analysis assistant."
        user_prompt = self._build_class_summary_prompt(structured_data)

        generation_log = {
            "chunk_type": "class",
            "structured_data": structured_data,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "raw_output": None,
            "summary": None,
            "success": False,
            "error": None
        }

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )

            content = response.choices[0].message.content
            generation_log["raw_output"] = content

            if content:
                summary = content.strip()
                generation_log["summary"] = summary
                generation_log["success"] = True
                self._save_generation_log(generation_log)
                return summary, generation_log

        except Exception as e:
            print(f"Warning: Failed to generate class summary: {e}")
            generation_log["error"] = str(e)
            self._save_generation_log(generation_log)
            return None, generation_log

    def generate_file_summary(self, structured_data: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Generate a summary for a file using compressed structured data.

        Args:
            structured_data: Compressed file info from PythonASTExtractor

        Returns:
            Tuple of (summary string or None, generation_log dict with prompt and output)
        """
        system_prompt = "You are a code analysis assistant."
        user_prompt = self._build_file_summary_prompt(structured_data)

        generation_log = {
            "chunk_type": "file",
            "structured_data": structured_data,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "raw_output": None,
            "summary": None,
            "success": False,
            "error": None
        }

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL_ID,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )

            content = response.choices[0].message.content
            generation_log["raw_output"] = content

            if content:
                summary = content.strip()
                generation_log["summary"] = summary
                generation_log["success"] = True
                self._save_generation_log(generation_log)
                return summary, generation_log

        except Exception as e:
            print(f"Warning: Failed to generate file summary: {e}")
            generation_log["error"] = str(e)
            self._save_generation_log(generation_log)
            return None, generation_log

    def _save_generation_log(self, log: Dict[str, Any]) -> None:
        """Save generation log to memory and optionally to file."""
        self.generation_logs.append(log)

        if self.save_logs and self.log_dir:
            import time
            timestamp = int(time.time() * 1000)
            chunk_type = log.get("chunk_type", "unknown")
            log_file = os.path.join(self.log_dir, f"summary_log_{chunk_type}_{timestamp}.json")
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(log, f, ensure_ascii=False, indent=2)

    def get_all_logs(self) -> List[Dict[str, Any]]:
        """Get all generation logs collected so far."""
        return self.generation_logs

    def save_all_logs(self, output_path: str) -> None:
        """Save all generation logs to a single JSON file."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.generation_logs, f, ensure_ascii=False, indent=2)

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

    def batch_generate_summaries(self, chunks: List[Any], max_workers: int = 5) -> Tuple[List[Any], List[Dict[str, Any]]]:
        """
        Generate summaries for a list of chunks in batch.
        Note: This is a placeholder - actual batch processing would need
        to handle API rate limits.

        Returns:
            Tuple of (updated chunks list, generation logs list)
        """
        # For now, process sequentially
        all_logs = []

        for chunk in chunks:
            if not hasattr(chunk, "structured_data") or not chunk.structured_data:
                continue

            chunk_type = chunk.chunk_type
            summary = None
            log = None

            if chunk_type == "function":
                summary, log = self.generate_function_summary(chunk.structured_data)
            elif chunk_type == "class":
                summary, log = self.generate_class_summary(chunk.structured_data)
            elif chunk_type == "file":
                summary, log = self.generate_file_summary(chunk.structured_data)

            if summary:
                chunk.summary = summary

            if log:
                all_logs.append(log)

        return chunks, all_logs
