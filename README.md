# RepoMind

代码感知的 RAG（检索增强生成）系统，用于仓库理解。

## 项目概述

RepoMind 是一个模块化的代码仓库理解系统，使用 RAG 技术来回答关于代码仓库的问题。

### 核心特性

- **代码感知的分块**: 基于 Python AST 的函数级代码分块
- **多阶段检索 Pipeline**: 查询扩展 + 向量搜索 + 元数据过滤 + 重排序
- **可扩展架构**: 向量存储抽象层，便于未来迁移到 Qdrant
- **FastAPI 服务**: 生产就绪的 API 接口

## 快速开始

### 环境要求

- Python 3.9+
- Conda 环境: `agentEnv`

### 安装依赖

```bash
conda activate agentEnv
pip install -r requirements.txt
```

### 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
# 编辑 .env 文件，设置 QWEN_API_KEY
```

### 使用核心接口（推荐）

直接使用统一的 `RepoMind` 类，提供所有可配置选项：

```python
from repomind import RepoMind

# 初始化（使用默认配置）
repomind = RepoMind()

# 或自定义配置
repomind = RepoMind(
    enable_query_expansion=True,      # 启用查询扩展
    enable_query_classification=True,  # 启用问题分类
    query_expansion_variants=2,         # 查询扩展变体数量
    use_fast_llm_for_expansion=True,    # 查询扩展用 fast LLM
    use_hybrid_answer_generation=True,  # 混合答案生成（简单问题用 fast）
)

# 索引仓库
repomind.index_repository("/path/to/repo")

# 查询
result = repomind.query("这个项目是做什么的？")
print(result["answer"])
```

### 运行 Demo 测试

```bash
conda activate agentEnv && python scripts/test_core.py
```

### 启动 API 服务

```bash
conda activate agentEnv && uvicorn repomind.api.main:app --reload
```

API 文档访问: http://localhost:8000/docs

## Demo 输出示例

以下是使用 `测试仓库/` 作为测试数据的实际运行输出：

### 查询 1: "这个项目是做什么的？"

```
Answer:
这个项目是一个基于大语言模型（LLM）的**智能旅行助手 Agent**。它实现了 ReAct（Reasoning + Acting）模式，能够理解用户请求，自主规划步骤并调用工具来完成任务。

主要功能模块如下：
1.  **提示词工程**：在 `prompt.py` 中定义了 `AGENT_SYSTEM_PROMPT`，设定了助手身份、可用工具列表及严格的输出格式（Thought-Action）。
2.  **模型调用**：通过 `ai_client.py` 中的 `OpenAICompatibleClient` 类及其 `generate` 函数，对接大语言模型 API 生成回复。
3.  **代理逻辑**：`agent.py` 是核心执行文件，负责维护对话历史，解析模型输出的行动指令，调用本地工具（如 `get_weather.py` 中的 `get_weather` 函数），并将执行结果（Observation）反馈给模型，形成闭环。
4.  **工具能力**：目前实现了查询天气（`get_weather`）和根据天气推荐景点（`get_attraction`）的功能。

参考文件：
- /测试仓库/prompt.py
- /测试仓库/ai_client.py
- /测试仓库/agent.py
- /测试仓库/get_weather.py

Sources:
  - /测试仓库/ai_client.py
  - /测试仓库/agent.py
  - /测试仓库/prompt.py
  - /测试仓库/get_weather.py

Latency: 40673.1ms
Tokens: 3560 (prompt: 2126, completion: 1434)
```

### 查询 2: "有哪些可用的工具函数？"

```
Answer:
根据提供的代码上下文，系统中主要定义了以下两个可用的工具函数，它们在 `agent.py` 的 `available_tools` 字典中被注册，并在 `prompt.py` 的系统提示中进行了说明：

1.  **`get_weather`**
    *   **功能**：查询指定城市的天气信息（目前支持上海、北京、广州、深圳、杭州等有限城市）。
    *   **定义位置**：`get_weather.py` 文件中的 `get_weather` 函数。

2.  **`get_attraction`**
    *   **功能**：根据城市和天气情况，使用 Tavily Search API 搜索并返回优化的旅游景点推荐。
    *   **定义位置**：`get_attraction.py` 文件中的 `get_attraction` 函数。

参考文件：
- /测试仓库/agent.py
- /测试仓库/get_weather.py
- /测试仓库/get_attraction.py
- /测试仓库/prompt.py

Sources:
  - /测试仓库/get_attraction.py
  - /测试仓库/ai_client.py
  - /测试仓库/prompt.py
  - /测试仓库/agent.py
  - /测试仓库/get_weather.py

Latency: 45240.9ms
Tokens: 3976 (prompt: 2323, completion: 1653)
```

### 查询 3: "OpenAICompatibleClient 类如何使用？"

```
Answer:
使用 `OpenAICompatibleClient` 类的步骤如下：

1.  **导入类**：从 `ai_client.py` 模块导入 `OpenAICompatibleClient`。
2.  **初始化实例**：调用 `__init__` 方法，传入 `model`、`api_key` 和 `base_url` 参数配置客户端。
3.  **生成响应**：调用 `generate` 方法，传入 `prompt`（用户提示）和 `system_prompt`（系统指令）参数获取模型返回的内容。

具体使用示例可见 `agent.py` 中的实例化与循环调用过程。

参考文件：
- /测试仓库/ai_client.py
- /测试仓库/agent.py

Sources:
  - /测试仓库/ai_client.py
  - /测试仓库/agent.py

Latency: 42964.7ms
Tokens: 3358 (prompt: 1721, completion: 1637)
```

## 项目结构

```
repomind/
├── repomind/
│   ├── ingestion/          # 数据解析与预处理
│   ├── indexing/           # 嵌入与向量索引
│   ├── storage/            # 向量存储抽象
│   ├── retrieval/          # 多阶段检索 pipeline
│   ├── generation/         # LLM 答案生成
│   ├── evaluation/         # 评估指标
│   ├── api/                # FastAPI 服务
│   └── configs/            # 配置管理
├── tests/                  # 测试套件
├── scripts/                # 工具脚本
├── 测试仓库/              # 测试用的示例仓库
├── requirements.txt
└── README.md
```

## API 使用

### 索引仓库

```bash
POST /index
{
  "repo_path": "/path/to/repository"
}
```

### 查询仓库

```bash
POST /query
{
  "question": "这个项目是做什么的？"
}
```

## 技术栈

- **向量存储**: FAISS
- **嵌入模型**: text-embedding-v4
- **LLM (强)**: qwen3.5-plus - 用于最终答案生成
- **LLM (快)**: qwen-flash - 用于查询扩展等低复杂度任务（为阶梯实现准备）
- **API 框架**: FastAPI
- **数据模型**: Pydantic

## 基线对比测试结果

以下是使用 `测试仓库/` 作为测试数据的四组系统对比结果：

### 系统说明

| 系统 | 特点 |
|------|------|
| LLM-only | 无检索 |
| Naive RAG | 文件级 chunk |
| Structured RAG | 函数级 chunk（但无 MQE/rerank） |
| Full System | 完整优化（qwen3.5-plus） |

### 对比结果汇总

#### 查询 1: "这个项目是做什么的？" (复杂问题)

| 系统 | Latency (ms) | Prompt Tokens | Completion Tokens | Total Tokens |
|------|--------------|---------------|--------------------|--------------|
| LLM-only | 24238.9 | 2212 | 1263 | 3475 |
| Naive RAG | 24691.1 | 2394 | 1641 | 4035 |
| Structured RAG | 21003.2 | 2128 | 1390 | 3518 |
| Full System | 30509.7 | 2126 | 1358 | 3484 |

#### 查询 2: "有哪些可用的工具函数？" (简单问题)

| 系统 | Latency (ms) | Prompt Tokens | Completion Tokens | Total Tokens |
|------|--------------|---------------|--------------------|--------------|
| LLM-only | 6674.4 | 2212 | 399 | 2611 |
| Naive RAG | 7367.0 | 2394 | 450 | 2844 |
| Structured RAG | 19543.7 | 2321 | 1373 | 3694 |
| Full System | 48906.6 | 2321 | 2211 | 4532 |

#### 查询 3: "OpenAICompatibleClient 类如何使用？" (复杂问题)

| 系统 | Latency (ms) | Prompt Tokens | Completion Tokens | Total Tokens |
|------|--------------|---------------|--------------------|--------------|
| LLM-only | 20367.4 | 2216 | 1379 | 3595 |
| Naive RAG | 8789.7 | 2397 | 563 | 2960 |
| Structured RAG | 20609.1 | 1719 | 1444 | 3163 |
| Full System | 69450.0 | 1719 | 3499 | 5218 |

#### 查询 4: "找到所有与天气相关的代码" (简单问题)

| 系统 | Latency (ms) | Prompt Tokens | Completion Tokens | Total Tokens |
|------|--------------|---------------|--------------------|--------------|
| LLM-only | 9254.2 | 2213 | 598 | 2811 |
| Naive RAG | 10535.3 | 2395 | 680 | 3075 |
| Structured RAG | 11211.7 | 2324 | 711 | 3035 |
| Full System | 26369.4 | 2322 | 629 | 2951 |

### 观察总结

- **Latency**: Full System 由于 MQE（多查询扩展）使用强 LLM，延迟较高，但答案质量通常更好
- **Token Usage**: 各系统差异不大，主要取决于生成的答案长度
- **答案质量**: Full System 和 Structured RAG 通常能提供更精确的答案，带正确的源文件引用

**注**：如需使用双模型策略（Fast LLM 用于查询扩展和分类），请直接使用统一的 `RepoMind` 核心接口。

**完整详细报告**请查看 `baseline_results/comparison_report.md` 和 `fast_llm_test_report.md`（本地留档，不提交 git）

## Full System 性能详细分析

对 Full System 进行了精细的 latency 统计，以下是各环节的耗时分析：

### 平均耗时 Breakdown (4 个查询平均)

| 阶段 | 平均耗时 (ms) | 占比 | 说明 |
|------|--------------|------|------|
| Query Expansion | 22,872 | 51.0% | LLM 生成查询变体（最大开销！）|
| Answer Generation | 21,135 | 47.1% | LLM 生成最终答案 |
| Embedding (3x) | 816 | 1.8% | 3 个查询的 embedding |
| Vector Search (3x) | 3 | 0.0% | FAISS 本地搜索（极快）|
| 其他 (merge/filter/rerank/pack) | 9 | 0.0% | 可忽略不计 |
| **Total** | **44,835** | **100%** | |

### 关键发现

1. **两个 LLM 调用占 98% 时间**：Query Expansion (51%) + Answer Generation (47%) 是绝对的主要开销
2. **本地操作极快**：FAISS 搜索、reranking、context packing 等本地操作加起来不到 10ms
3. **优化方向**：如果要降低 latency，优先考虑：
   - 缓存查询扩展结果
   - 使用更快的模型做查询扩展（**已准备 qwen-flash**）
   - 或直接去掉 MQE（牺牲召回率换速度）

## Fast LLM 阶梯实现（已完成！）

已成功实现双模型策略，测试结果如下：

### 性能对比

| 指标 | 原版 Full System | Fast LLM 版本 | 改善 |
|------|-----------------|--------------|------|
| Query Expansion 延迟 | ~22,800 ms | ~550 ms | **97.6% ↓** |
| 简单问题总延迟 | ~45,000 ms | ~7,000 ms | **84.4% ↓** |
| 复杂问题总延迟 | ~45,000 ms | ~19,000 ms | **57.8% ↓** |

### 实现方案

1. **Query Expansion** → 使用 **qwen-flash**
   - 简化提示词，限制输出格式
   - 降低 temperature (0.3)，提高确定性
   - 延迟从 22.8s → 0.55s

2. **Query Classification** → 使用 **qwen-flash**
   - 简单提示词：只返回 "simple" 或 "complex"
   - 极低 temperature (0.1)，输出稳定
   - 延迟仅 ~400ms

3. **Answer Generation** → 智能选择
   - **简单问题**：用 **qwen-flash**（~5-7s）
   - **复杂问题**：用 **qwen3.5-plus**（~8-27s）

### 问题分类规则

- **简单问题**：问"是什么"、"找文件"、"变量名/函数名"、"列举清单"
- **复杂问题**：问"为什么"、"如何实现"、"业务逻辑"、"项目做什么"、"详细解释"

### 新增/修改的文件

- **修改**: `repomind/retrieval/query_expander.py` - 简化提示词，支持自定义模型
- **新增**: `repomind/retrieval/query_classifier.py` - 问题分类器
- **修改**: `repomind/generation/answer_generator.py` - 支持双 LLM Service
- **新增**: `repomind/baselines/full_system_fast.py` - Fast LLM 版本
- **新增**: `scripts/test_fast_llm.py` - 测试脚本

**完整测试数据**请查看 `baseline_results/fast_llm_test_report.md` 和 `fast_llm_test_results.json`（本地留档，不提交 git）

## 开发进度

- [x] Phase 1: 核心基础设施
- [x] Phase 2: 数据模型与摄入
- [x] Phase 3: 嵌入与存储
- [x] Phase 4: 检索 Pipeline
- [x] Phase 5: 生成模块
- [x] Phase 6: 评估与 API
- [x] Phase 7: 文档与提交
- [x] Phase 8: 基线对比测试
- [x] Phase 9: Fast LLM 阶梯实现

## 许可证

MIT License
