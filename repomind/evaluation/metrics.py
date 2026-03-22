import time
from typing import List, Dict, Any, Callable
from functools import wraps


class Metrics:
    """Simple metrics for Demo phase: latency and token usage."""

    @staticmethod
    def latency(func: Callable) -> Callable:
        """Decorator to measure function latency."""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000

            if isinstance(result, dict):
                result["latency_ms"] = latency_ms
            else:
                result = {
                    "result": result,
                    "latency_ms": latency_ms
                }
            return result
        return wrapper

    @staticmethod
    def calculate_token_efficiency(prompt_tokens: int, completion_tokens: int) -> Dict[str, float]:
        """Calculate token efficiency metrics."""
        total_tokens = prompt_tokens + completion_tokens
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "completion_ratio": completion_tokens / max(prompt_tokens, 1)
        }

    @staticmethod
    def aggregate_metrics(metrics_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate metrics from multiple runs."""
        if not metrics_list:
            return {}

        latencies = [m.get("latency_ms", 0) for m in metrics_list if "latency_ms" in m]
        prompt_tokens_list = [m.get("prompt_tokens", 0) for m in metrics_list if "prompt_tokens" in m]
        completion_tokens_list = [m.get("completion_tokens", 0) for m in metrics_list if "completion_tokens" in m]

        aggregated = {}
        if latencies:
            aggregated["avg_latency_ms"] = sum(latencies) / len(latencies)
            aggregated["min_latency_ms"] = min(latencies)
            aggregated["max_latency_ms"] = max(latencies)

        if prompt_tokens_list:
            aggregated["avg_prompt_tokens"] = sum(prompt_tokens_list) / len(prompt_tokens_list)
            aggregated["total_prompt_tokens"] = sum(prompt_tokens_list)

        if completion_tokens_list:
            aggregated["avg_completion_tokens"] = sum(completion_tokens_list) / len(completion_tokens_list)
            aggregated["total_completion_tokens"] = sum(completion_tokens_list)

        return aggregated
