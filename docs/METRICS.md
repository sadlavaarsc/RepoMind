# Evaluation Metrics

## Test Suite Overview

This test suite evaluates RepoMind on two representative codebases:

### 1. travel_agent (small)
- **Project Type**: LLM-based travel assistant agent using ReAct pattern
- **Location**: `测试仓库/旅行agent/`
- **Size**: Small, ~5 Python files
- **Questions**: 10 questions (4 simple, 3 medium, 3 complex)

### 2. cuezero (medium-large)
- **Project Type**: High-performance billiards AI system with deep RL + MCTS
- **Location**: `测试仓库/CueZero/` (not included in git)
- **Size**: Medium-large, ~50+ files
- **Questions**: 10 questions (4 simple, 3 medium, 3 complex)

### Question Difficulty Classification

| Difficulty | Description |
|------------|-------------|
| **Simple** | Basic understanding, single-file lookup |
| **Medium** | Cross-file understanding, function relationships |
| **Complex** | Architectural understanding, multiple file analysis |

### Example Output

#### Query 1 (travel_agent, simple)
**Question**: "这个项目是做什么的？" (What does this project do?)

**Full System Answer**:
> 这个项目是一个基于大语言模型（LLM）的智能旅行助手 Agent。它实现了 ReAct（Reasoning + Acting）模式，能够理解用户请求，自主规划步骤并调用工具来完成任务。
>
> 参考文件：
> - agent.py
> - prompt.py
> - ai_client.py
> - get_weather.py

**Token Usage**: 2845 total tokens (Full System)

---

#### Query 2 (cuezero, simple)
**Question**: "CueZero 是什么项目？" (What is CueZero?)

**Full System Answer**:
> CueZero 是一个高性能台球 AI 系统，它将深度强化学习与专门设计的连续动作蒙特卡洛树搜索（MCTS）相结合。该项目旨在解决高维连续状态和动作空间中的决策难题，并处理复杂的物理动力学。
>
> 其核心特点包括：
> - **架构**: 遵循受 AlphaZero 启发的神经引导搜索架构，但针对连续动作空间进行了适配。
> - **训练**: 使用三阶段训练流程，结合监督预训练与自我对弈强化学习。
> - **性能**: 模型紧凑（约 160K 参数），对抗规则型基线 Agent 胜率达 95%。
>
> 参考文件：
> - README.md
> - README_zh.md
> - docs/HOW_IT_WORKS.md

**Token Usage**: 2325 total tokens (Full System)

---

## Retrieval Metrics

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
