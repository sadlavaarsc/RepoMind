# Core Modules

## 1. Ingestion

**Location**: `repomind/ingestion/`

- **chunker.py**: Multi-level code chunker
  - file level: Whole module overview
  - class level: Class responsibilities and methods
  - function level: Function inputs, outputs, and call relationships
  - block level: Code blocks in script files

- **summary_generator.py**: LLM summary generator
  - Uses qwen-flash for fast generation
  - Uses only structured data, not full code
  - Summary included in embedding text

- **models.py**: CodeChunk data model
  - chunk_type, name, signature, docstring
  - summary, structured_data
  - embedding_text (for embeddings)

## 2. Retrieval

**Location**: `repomind/retrieval/`

- **pipeline.py**: Multi-stage retrieval pipeline
  - Query expansion (MQE)
  - Vector search
  - Reranking

- **query_expander.py**: Query expander
  - Supports custom models
  - Generates multiple query variants

- **query_classifier.py**: Query classifier
  - simple/complex binary classification
  - Used for dual model strategy

- **reranker.py**: Reranker (Latest optimization!)
  - Bucket guarantee: At least 1 document + 1 code
  - Chinese optimization: 2-gram + 3-gram matching
  - Meaningless word filter: Chinese pronoun exclusion table
  - MMR diversity: Maximal Marginal Relevance
  - Weight tuning: alpha=0.85 (cosine), beta=0.15 (keywords)

## 3. Generation

**Location**: `repomind/generation/`

- **answer_generator.py**: Answer generator
  - Supports dual LLM Service
  - Smart model selection

- **llm_service.py**: LLM service wrapper
  - OpenAI compatible interface
  - Supports custom base_url and model

## 4. Evaluation

**Location**: `repomind/evaluation/`

- **retrieval_metrics.py**: Retrieval metrics
  - Recall
  - Hit Rate
  - Precision

- **llm_evaluator.py**: LLM answer evaluation
  - Sufficiency
  - Correctness
  - Grounding

- **llm_metrics.py**: LLM metrics aggregation
  - Answerable Rate
  - End-to-end Success Rate
  - Retrieval Gap
