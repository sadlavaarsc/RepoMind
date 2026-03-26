# 核心模块

## 1. Ingestion（数据摄入）

**位置**：`repomind/ingestion/`

- **chunker.py**：多级代码分块器
  - file 级：整个模块概览
  - class 级：类的职责和方法
  - function 级：函数的输入输出和调用关系
  - block 级：脚本文件中的代码块

- **summary_generator.py**：LLM 摘要生成器
  - 使用 qwen-flash 快速生成
  - 仅用结构化数据，不用完整代码
  - 摘要内容包含在嵌入文本中

- **models.py**：CodeChunk 数据模型
  - chunk_type, name, signature, docstring
  - summary, structured_data
  - embedding_text（用于嵌入）

## 2. Retrieval（检索）

**位置**：`repomind/retrieval/`

- **pipeline.py**：多阶段检索 Pipeline
  - 查询扩展 (MQE)
  - 向量搜索
  - 重排序

- **query_expander.py**：查询扩展器
  - 支持自定义模型
  - 生成多个查询变体

- **query_classifier.py**：查询分类器
  - simple/complex 二分类
  - 用于双模型策略

- **reranker.py**：重排序器（最新优化！）
  - 分桶保证：至少 1 个文档 + 1 个代码
  - 中文优化：2-gram + 3-gram 匹配
  - 无意义词过滤：中文代词排除表
  - MMR 多样性：Maximal Marginal Relevance
  - 权重调整：alpha=0.85（余弦），beta=0.15（关键词）

## 3. Generation（答案生成）

**位置**：`repomind/generation/`

- **answer_generator.py**：答案生成器
  - 支持双 LLM Service
  - 智能选择模型

- **llm_service.py**：LLM 服务封装
  - OpenAI 兼容接口
  - 支持自定义 base_url 和 model

## 4. Evaluation（评估）

**位置**：`repomind/evaluation/`

- **retrieval_metrics.py**：检索指标
  - 召回率
  - 命中率
  - 精确率

- **llm_evaluator.py**：LLM 答案评估
  - 充分性
  - 正确性
  - 事实性

- **llm_metrics.py**：LLM 指标聚合
  - 可回答率
  - 端到端成功率
  - 检索差距
