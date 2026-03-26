# Evaluation Metrics

## Retrieval Metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **Recall** | Fraction of relevant chunks retrieved | `|Retrieved ∩ Relevant| / |Relevant|` |
| **Hit Rate** | Fraction of questions with at least one relevant chunk | `1.0 if |Retrieved ∩ Relevant| > 0 else 0.0` |
| **Precision** | Fraction of retrieved chunks that are relevant | `|Retrieved ∩ Relevant| / |Retrieved|` |

All retrieval metrics are calculated at the file level using source file paths. See `repomind/evaluation/retrieval_metrics.py` for implementation details.

## LLM Evaluation Metrics

LLM-based evaluation uses qwen-flash to assess answer quality in three dimensions:

| Metric | Scale | Definition |
|--------|-------|------------|
| **Sufficiency** | 0-2 | Is the retrieved context sufficient to answer the question?<br/>2 = Fully sufficient, 1 = Partially sufficient, 0 = Not sufficient |
| **Correctness** | 0-2 | Is the answer correct and complete compared to ground truth?<br/>2 = Correct and complete, 1 = Partially correct, 0 = Incorrect |
| **Grounding** | 0-2 | Are all claims in the answer supported by the context?<br/>2 = Fully grounded, 1 = Partially grounded, 0 = Not grounded |

See `repomind/evaluation/llm_evaluator.py` for the prompt templates and evaluation logic.

## Aggregate Metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **Answerable Rate** | Fraction of questions with sufficiency == 2 | `count(sufficiency == 2) / N` |
| **End-to-end Success Rate** | Fraction of questions with correctness == 2 AND grounding == 2 | `count(correctness == 2 AND grounding == 2) / N` |
| **Retrieval Gap** | Average gap between sufficiency and correctness | `avg(sufficiency - correctness)` |
| **Avg Sufficiency** | Average sufficiency score across all questions | `sum(sufficiency) / N` |
| **Avg Correctness** | Average correctness score across all questions | `sum(correctness) / N` |
| **Avg Grounding** | Average grounding score across all questions | `sum(grounding) / N` |

See `repomind/evaluation/llm_metrics.py` for implementation details.

## Performance Metrics

| Metric | Definition |
|--------|------------|
| **Avg Latency** | Average query response time in milliseconds |
| **Avg Total Token** | Average total tokens consumed per query (prompt + completion) |
| **Avg Prompt Token** | Average prompt tokens per query |
| **Avg Completion Token** | Average completion tokens per query |
