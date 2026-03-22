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

### 运行 Demo 测试

```bash
conda activate agentEnv && python scripts/test_demo.py
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
- **LLM**: qwen3.5-plus
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

## 许可证

MIT License
