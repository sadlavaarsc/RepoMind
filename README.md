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
