# RepoMind Project CLAUDE.md

## 项目概述
RepoMind 是一个代码感知的 RAG（检索增强生成）系统，用于仓库理解。

## 关键文件位置
- **需求文档**: `/Users/liwentao/Documents/开发/RepoMind/要求.md`
- **API 配置**: `/Users/liwentao/Documents/开发/RepoMind/api_key.md`
- **测试仓库**: `/Users/liwentao/Documents/开发/RepoMind/测试仓库/`

## 环境要求
- Conda 环境: `agentEnv`（所有 Python 命令需使用 `conda activate agentEnv && ...` 形式）

## API 配置
- Base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- API Key 环境变量: `QWEN_API_KEY`
- LLM 模型: `qwen3.5-plus`
- 嵌入模型: `text-embedding-v4`

## 开发进度
- [x] Phase 1: 核心基础设施
- [x] Phase 2: 数据模型与摄入
- [x] Phase 3: 嵌入与存储
- [x] Phase 4: 检索 Pipeline
- [x] Phase 5: 生成模块
- [x] Phase 6: 评估与 API
- [x] Phase 7: 文档与提交

## Demo 开发已完成

所有核心模块已实现：
- 摄入模块（Python AST 解析）
- 嵌入与存储（FAISS）
- 检索 Pipeline（多阶段）
- 生成模块（LLM 答案生成）
- API 层（FastAPI）
- Demo 测试脚本

## 下一步

1. 配置 `.env` 文件，设置 `QWEN_API_KEY`
2. 运行 `python scripts/test_demo.py` 测试
3. 或启动 API 服务: `uvicorn repomind.api.main:app --reload`

## 测试仓库内容
测试仓库是一个简单的旅行助手代理项目，包含：
- `ai_client.py` - OpenAI 兼容客户端
- `agent.py` - 旅行助手代理主循环
- `get_weather.py` - 天气查询工具
- `get_attraction.py` - 景点推荐工具
- `prompt.py` - Agent 系统提示词

## 注意事项
- Demo 阶段不需要完整 baseline 测试
- 专注于实现简单 repo 解释任务
