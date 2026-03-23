 import time
import pytest
from repomind.evaluation.metrics import Metrics


def test_latency_decorator():
    """Test latency measurement decorator."""
    metrics = Metrics()

    @metrics.latency
    def slow_function():
        time.sleep(0.01)
        return {"result": "done"}

    result = slow_function()
    assert "latency_ms" in result
    assert result["latency_ms"] >= 10


def test_token_efficiency():
    """Test token efficiency calculation."""
    result = Metrics.calculate_token_efficiency(100, 50)
    assert result["prompt_tokens"] == 100
    assert result["completion_tokens"] == 50
    assert result["total_tokens"] == 150


def test_aggregate_metrics():
    """Test metrics aggregation."""
    metrics_list = [
        {"latency_ms": 100, "prompt_tokens": 10, "completion_tokens": 20},
        {"latency_ms": 200, "prompt_tokens": 20, "completion_tokens": 30},
    ]
    aggregated = Metrics.aggregate_metrics(metrics_list)
    assert aggregated["avg_latency_ms"] == 150
    assert aggregated["total_prompt_tokens"] == 30
