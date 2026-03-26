# RepoMind

代码感知的 RAG（检索增强生成）系统，用于仓库理解。

## 项目概述

RepoMind 是一个模块化的代码仓库理解系统，使用 RAG 技术来回答关于代码仓库的问题。

### 核心特性

- **多级代码感知分块**: 基于 Python AST 的 file/class/function/block 多级分块，带结构化数据提取
- **LLM 摘要生成**: 建库时自动为每个 chunk 生成 LLM 摘要，提升检索质量
- **多阶段检索 Pipeline**: 查询扩展 + 向量搜索 + 元数据过滤 + 重排序
- **中文关键词优化**: 支持中文 2-gram + 3-gram 匹配，无意义代词排除
- **混合答案生成**: 简单问题用 fast 模型，复杂问题用 strong 模型
- **可扩展架构**: 向量存储抽象层，便于未来迁移到 Qdrant
- **FastAPI 服务**: 生产就绪的 API 接口
- **MCP 服务**: 支持 Model Context Protocol，便于接入其他 AI 工具

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

### 启动 MCP 服务

RepoMind 支持 MCP (Model Context Protocol)，可以轻松接入 Claude Desktop 等支持 MCP 的 AI 工具：

```bash
conda activate agentEnv && python scripts/start_mcp_server.py
```

**MCP 工具列表**:
- `index_repository(repo_path)` - 索引代码仓库
- `query_repository(question)` - 查询已索引的仓库
- `get_health()` - 检查服务健康状态
- `save_index(index_path)` - 保存索引到磁盘
- `load_index(index_path)` - 从磁盘加载索引

**Claude Desktop 配置示例**:
在 Claude Desktop 的配置文件中添加：
```json
{
  "mcpServers": {
    "repomind": {
      "command": "conda",
      "args": ["run", "-n", "agentEnv", "python", "/path/to/RepoMind/scripts/start_mcp_server.py"]
    }
  }
}
```

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         RepoMind 系统架构                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   查询输入    │ →  │  查询扩展     │ →  │  查询分类     │   │
│  │  (Query)     │    │  (MQE)       │    │  (Classifier) │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│         ↓                   ↓                   ↓              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  多阶段检索 Pipeline                       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  1. 向量检索 (FAISS) → Top 20                           │  │
│  │  2. 分桶保证 (文档+代码)                                 │  │
│  │  3. 关键词打分 (中文 n-gram + 无意义词过滤)              │  │
│  │  4. MMR 重排序 (多样性保证)                              │  │
│  │  5. 最终选择 (Top 5)                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  上下文构建                                │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  - Chunk Summary (LLM 生成)                              │  │
│  │  - Structured Data (imports, signatures, calls)         │  │
│  │  - 原始代码 (可选)                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│         ↓                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  答案生成 (双模型策略)                     │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  简单问题 → qwen-flash (快速)                            │  │
│  │  复杂问题 → qwen3.5-plus (高质量)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│         ↓                                                        │
│  ┌──────────────┐                                               │
│  │   答案输出    │                                               │
│  │  (Answer)    │                                               │
│  └──────────────┘                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 核心模块说明

### 1. Ingestion (数据摄入)

**位置**: `repomind/ingestion/`

- **chunker.py**: 多级代码分块器
  - file 级: 整个模块概览
  - class 级: 类的职责和方法
  - function 级: 函数的输入输出和调用关系
  - block 级: 脚本文件中的代码块

- **summary_generator.py**: LLM 摘要生成器
  - 使用 qwen-flash 快速生成
  - 仅用结构化数据，不用完整代码
  - 摘要内容包含在嵌入文本中

- **models.py**: CodeChunk 数据模型
  - chunk_type, name, signature, docstring
  - summary, structured_data
  - embedding_text (用于嵌入)

### 2. Retrieval (检索)

**位置**: `repomind/retrieval/`

- **pipeline.py**: 多阶段检索 Pipeline
  - 查询扩展 (MQE)
  - 向量搜索
  - 重排序

- **query_expander.py**: 查询扩展器
  - 支持自定义模型
  - 生成多个查询变体

- **query_classifier.py**: 查询分类器
  - simple/complex 二分类
  - 用于双模型策略

- **reranker.py**: 重排序器 (最新优化!)
  - 分桶保证: 至少 1 个文档 + 1 个代码
  - 中文优化: 2-gram + 3-gram 匹配
  - 无意义词过滤: 中文代词排除表
  - MMR 多样性: Maximal Marginal Relevance
  - 权重调整: alpha=0.85 (余弦), beta=0.15 (关键词)

### 3. Generation (答案生成)

**位置**: `repomind/generation/`

- **answer_generator.py**: 答案生成器
  - 支持双 LLM Service
  - 智能选择模型

- **llm_service.py**: LLM 服务封装
  - OpenAI 兼容接口
  - 支持自定义 base_url 和 model

### 4. Evaluation (评估)

**位置**: `repomind/evaluation/`

- **retrieval_metrics.py**: 检索指标
  - 召回率 (Recall)
  - 命中率 (Hit Rate)
  - 精确率 (Precision)

- **llm_evaluator.py**: LLM 答案评估
  - 充分性 (Sufficiency)
  - 正确性 (Correctness)
  - 事实性 (Grounding)

- **llm_metrics.py**: LLM 指标聚合
  - 可回答率
  - 端到端成功率
  - 检索差距

## 完整基线测试结果 (2026-03-26)

### 测试项目

1. **travel_agent** (小项目): 基于 LLM 的旅行助手 Agent
2. **cuezero** (中大型项目): 高性能台球 AI 系统

### 测试系统

| 系统 | 特点 |
|------|------|
| LLM-only | 无检索 |
| Naive RAG | 文件级 chunk |
| Structured RAG | 函数级 chunk |
| Full System | 完整优化（qwen3.5-plus） |
| Full System Fast | 完整优化 + 双模型策略（qwen-flash + qwen3.5-plus） |

### travel_agent 项目结果

| 系统 | 平均召回率 | 平均命中率 | 可回答率 | 端到端成功率 | 平均正确性 | 平均事实性 | 平均总Token | 平均延迟(ms) |
|------|-----------|-----------|---------|------------|-----------|-----------|-----------|------------|
| llm_only | 0.000 | 0.000 | 0.0% | 40.0% | 2.00 | 0.80 | 3136 | 14463.6 |
| naive_rag | 1.000 | 1.000 | 90.0% | 100.0% | 2.00 | 2.00 | 3163 | 12789.5 |
| structured_rag | 0.975 | 1.000 | 80.0% | 100.0% | 2.00 | 2.00 | 2686 | 13869.1 |
| full_system | 0.975 | 1.000 | 90.0% | 100.0% | 2.00 | 2.00 | 2845 | 37362.6 |
| full_system_fast | 0.975 | 1.000 | 90.0% | 100.0% | 2.00 | 2.00 | 2502 | 15157.2 |

### cuezero 项目结果

| 系统 | 平均召回率 | 平均命中率 | 可回答率 | 端到端成功率 | 平均正确性 | 平均事实性 | 平均总Token | 平均延迟(ms) |
|------|-----------|-----------|---------|------------|-----------|-----------|-----------|------------|
| llm_only | 0.000 | 0.000 | 0.0% | 50.0% | 2.00 | 1.00 | 3590 | 21760.5 |
| naive_rag | 0.500 | 1.000 | 100.0% | 100.0% | 2.00 | 2.00 | 14100 | 15034.3 |
| structured_rag | 0.400 | 0.900 | 70.0% | 70.0% | 1.70 | 2.00 | 3420 | 20691.7 |
| full_system | 0.450 | 1.000 | 100.0% | 80.0% | 1.70 | 2.00 | 2313 | 48915.8 |
| full_system_fast | 0.450 | 1.000 | 100.0% | 90.0% | 1.80 | 2.00 | 1634 | 14342.8 |

### 关键改进 (chinese_rerank_fix)

1. **中文关键词匹配优化**
   - 添加 2-gram + 3-gram 匹配
   - 无意义代词排除表 ("我", "我们", "你", "你们" 等)
   - README_zh.md 现在能正确被检索出来了!

2. **权重调整**
   - alpha=0.85 (余弦相似度权重)
   - beta=0.15 (关键词分数权重)
   - 关键词分数作为"锦上添花"，不是主要决定因素

3. **分桶保证**
   - 至少 1 个文档 chunk
   - 至少 1 个代码 chunk
   - 确保检索结果的多样性

## 项目结构

```
repomind/
├── repomind/
│   ├── ingestion/          # 数据解析与预处理
│   │   ├── chunker.py      # 多级代码分块器
│   │   ├── summary_generator.py  # LLM 摘要生成
│   │   └── models.py       # CodeChunk 数据模型
│   ├── indexing/           # 嵌入与向量索引
│   │   └── embedding_service.py
│   ├── storage/            # 向量存储抽象
│   │   ├── vector_store.py # 抽象基类
│   │   └── faiss_store.py  # FAISS 实现
│   ├── retrieval/          # 多阶段检索 pipeline
│   │   ├── pipeline.py     # 检索主流程
│   │   ├── query_expander.py  # 查询扩展
│   │   ├── query_classifier.py  # 查询分类
│   │   └── reranker.py     # 重排序器 (中文优化)
│   ├── generation/         # LLM 答案生成
│   │   ├── answer_generator.py
│   │   └── llm_service.py
│   ├── evaluation/         # 评估指标
│   │   ├── retrieval_metrics.py
│   │   ├── llm_evaluator.py
│   │   ├── llm_metrics.py
│   │   └── result_parser.py
│   ├── api/                # FastAPI 服务
│   │   ├── main.py
│   │   └── schemas.py
│   ├── mcp/                # MCP 服务
│   │   └── server.py
│   ├── configs/            # 配置管理
│   │   └── settings.py
│   ├── baselines/          # 基线系统
│   │   ├── naive_rag.py
│   │   ├── structured_rag.py
│   │   ├── full_system.py
│   │   └── full_system_fast.py
│   └── core.py             # RepoMind 核心类
├── test_suite/             # 测试集
│   ├── travel_agent/
│   │   ├── test_questions.json
│   │   ├── test_questions.md
│   │   └── expected_sources.json
│   └── cuezero/
│       ├── test_questions.json
│       ├── test_questions.md
│       └── expected_sources.json
├── scripts/                # 工具脚本
│   ├── run_baseline_comparison.py
│   ├── analyze_baseline_results.py
│   ├── run_full_llm_eval.py
│   ├── start_mcp_server.py
│   └── ...
├── tests/                  # 测试套件
│   ├── test_api.py
│   ├── test_storage.py
│   └── ...
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
- **LLM (快)**: qwen-flash - 用于查询扩展、问题分类、chunk 摘要生成、LLM 评估
- **API 框架**: FastAPI
- **数据模型**: Pydantic

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
- [x] Phase 10: 多级 Chunk + LLM Summary
- [x] Phase 11: 中文 Reranker 优化
- [x] Phase 12: 项目完善与收尾 (FAISS 增强 / MCP 服务 / 文档更新)

## 重要更新记录

### 2026-03-26: 项目完善与收尾

**关键改进**:
- **FAISS 中间层增强**: 添加 delete、update、clear、get_chunks_by_file、count、exists 等方法
- **MCP 服务支持**: 新增 MCP (Model Context Protocol) 服务器，便于接入 Claude Desktop 等 AI 工具
- **FastAPI 单元测试**: 添加 API 端点测试
- **README 更新**: 完善基线测试结果表格，增加平均正确性、平均事实性、平均总Token 指标

**新增文件**:
- `repomind/mcp/server.py` - MCP 服务器
- `scripts/start_mcp_server.py` - MCP 服务启动脚本
- `tests/test_api.py` - FastAPI 单元测试

### 2026-03-26: 中文 Reranker 优化

**关键改进**:
- 添加中文 2-gram + 3-gram 匹配
- 添加中文无意义代词排除表
- 调整权重：alpha=0.85 (余弦相似度), beta=0.15 (关键词分数)
- README_zh.md 现在能正确被检索出来了

**测试结果**:
- travel_agent: 召回率 0.975, 命中率 1.000, 端到端成功率 100.0%
- cuezero: 召回率 0.450, 命中率 1.000, 可回答率 100.0%

### 2026-03-24: 多级 Chunk + LLM Summary

**关键改进**:
- 多级 chunk 架构（file / class / function / block）
- 结构化信息提取（imports、signatures、calls 等）
- LLM 摘要生成框架（使用 qwen-flash 模型）
- 建库时自动生成 LLM summaries

### 2026-03-23: Chunker Bug 修复

**修复的 Bug**:
- 重复的 Chunk - 类方法被提取两次的问题
- `_is_top_level` 永远返回 True - 已添加 parent 属性设置
- 缺少模块级上下文 - 现在支持多级 chunk
- 纯脚本文件无法切分 - 增加了脚本块切分支持

## 许可证

MIT License
