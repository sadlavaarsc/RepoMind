# Evaluation Metrics

## Test Suite Overview

This test suite evaluates RepoMind on two representative codebases. Test questions are stored in JSON format under `test_suite/`.

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

#### Simple Query (travel_agent)
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

#### Complex Query (cuezero)
**Question**: "详细解释 MCTS 搜索是如何为连续动作空间优化的？" (How is MCTS search optimized for continuous action spaces?)

**Full System Answer**:
> ## MCTS 连续动作空间优化详解
>
> CueZero 的 MCTS 针对连续动作空间（台球击球参数）进行了专门优化，主要通过以下四个关键创新：
>
> ### 1. 启发式动作生成（Ghost Ball 方法）
>
> 传统 MCTS 对连续空间随机采样效率低，CueZero 使用几何启发式生成高质量候选动作：
>
> - **Ghost Ball 计算**：通过目标球到袋口的向量，计算理想击球角度
> - **候选动作生成**：为每个目标球 - 袋口组合生成理想击球及微小扰动变体
> - **效果**：生成约 30 个高质量候选动作，而非随机采样
>
> ### 2. 策略网络引导的剪枝
>
> 生成候选动作后，使用策略网络进一步筛选，保留前 2/3 的动作，减少约 66% 的低价值动作，加速收敛。
>
> ### 3. 混合价值估计
>
> 结合神经网络预测与物理模拟结果：
> - 浅层深度：物理模拟准确且速度可接受
> - 深层深度：网络预测快速，避免模拟误差累积
>
> ### 4. 动态搜索策略
>
> | 模式 | 模拟次数 | 最大深度 | 超时 | 候选动作 | 决策时间 |
> |------|---------|---------|------|---------|---------|
> | MCTS-Full | 150 | 4 | 15s | ~30 | ~3 分钟 |
> | MCTS-Fast | 30 | 2 | 3s | ~10 | ~1 秒 |
>
> 参考文件：
> - cuezero/mcts/search.py（MCTS 类定义）
> - docs/HOW_IT_WORKS.md（连续动作 MCTS 详细说明）
> - docs/TRAINING.md（训练阶段优化策略）

**Token Usage**: 3272 total tokens (Full System)

---

## Retrieval Metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **Recall** | Fraction of relevant chunks retrieved | \|Retrieved ∩ Relevant\| / \|Relevant\| |
| **Hit Rate** | Fraction of questions with at least one relevant chunk | 1.0 if \|Retrieved ∩ Relevant\| > 0 else 0.0 |
| **Precision** | Fraction of retrieved chunks that are relevant | \|Retrieved ∩ Relevant\| / \|Retrieved\| |

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
| **Answerable Rate** | Fraction of questions with sufficiency == 2 | count(sufficiency == 2) / N |
| **End-to-end Success Rate** | Fraction of questions with correctness == 2 AND grounding == 2 | count(correctness == 2 AND grounding == 2) / N |
| **Retrieval Gap** | Average gap between sufficiency and correctness | avg(sufficiency - correctness) |
| **Avg Sufficiency** | Average sufficiency score across all questions | sum(sufficiency) / N |
| **Avg Correctness** | Average correctness score across all questions | sum(correctness) / N |
| **Avg Grounding** | Average grounding score across all questions | sum(grounding) / N |

See `repomind/evaluation/llm_metrics.py` for implementation details.

## Performance Metrics

| Metric | Definition |
|--------|------------|
| **Avg Latency** | Average query response time in milliseconds |
| **Avg Total Token** | Average total tokens consumed per query (prompt + completion) |
| **Avg Prompt Token** | Average prompt tokens per query |
| **Avg Completion Token** | Average completion tokens per query |
