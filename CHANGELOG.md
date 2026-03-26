# Changelog

All notable changes to RepoMind will be documented in this file.

## 2026-03-26: README Enhancement & Test Updates

### New Features
- Created bilingual README (README.md + README_zh.md)
- Added tech stack badges (Python, FastAPI, FAISS, Pydantic, OpenAI SDK, MCP)
- Added Mermaid system architecture diagram
- Added comprehensive evaluation metrics documentation
- Added new evaluation modules:
  - `llm_evaluator.py` - LLM-based answer quality evaluator
  - `llm_metrics.py` - LLM metrics aggregation
  - `result_parser.py` - Result parser

### Improvements
- Updated test files with new test cases:
  - `test_ingestion.py`: Added new fields test and get_embedding_text() test
  - `test_retrieval.py`: Added Chinese keyword matching test and bucket guarantee test
  - `test_storage.py`: Added count, exists, get_chunks_by_file, delete, update, clear method tests

### Documentation
- Added "Problem & Use Cases" section to clarify business requirements
- Added "Technical Highlights" section detailing:
  - Chunker design (multi-level chunking trade-off)
  - Reranker design (Chinese optimization, bucket guarantee, MMR)
  - Token efficiency optimization (LLM Summary, dual model strategy)

---

## 2026-03-26: Project Completion & Finalization

### Key Improvements
- **FAISS Middleware Enhancement**: Added delete, update, clear, get_chunks_by_file, count, exists methods
- **MCP Service Support**: Added MCP (Model Context Protocol) server for easy integration with Claude Desktop and other AI tools
- **FastAPI Unit Tests**: Added API endpoint tests
- **README Update**: Enhanced baseline results table with Avg Correctness, Avg Grounding, Avg Total Token metrics

### New Files
- `repomind/mcp/server.py` - MCP server
- `scripts/start_mcp_server.py` - MCP service startup script
- `tests/test_api.py` - FastAPI unit tests

---

## 2026-03-26: Chinese Reranker Optimization

### Key Improvements
- Added Chinese 2-gram + 3-gram matching
- Added Chinese meaningless pronoun exclusion table
- Adjusted weights: alpha=0.85 (cosine similarity), beta=0.15 (keyword score)
- README_zh.md can now be correctly retrieved

### Test Results
- travel_agent: Recall 0.975, Hit Rate 1.000, E2E Success Rate 100.0%
- cuezero: Recall 0.450, Hit Rate 1.000, Answerable Rate 100.0%

---

## 2026-03-24: Multi-level Chunk + LLM Summary

### Key Improvements
- Multi-level chunk architecture (file / class / function / block)
- Structured information extraction (imports, signatures, calls, etc.)
- LLM summary generation framework (using qwen-flash model)
- Automatic LLM summaries generation during indexing

---

## 2026-03-23: Chunker Bug Fixes

### Fixed Bugs
- **Duplicate Chunks**: Issue where class methods were extracted twice
- **`_is_top_level` always returning True**: Added parent attribute setting to correctly distinguish class methods from top-level functions
- **Missing module-level context**: Now supports multi-level chunks
- **Pure script files couldn't be chunked**: Added script block chunking support

---

## Development Progress Tracking

- [x] Phase 1: Core Infrastructure
- [x] Phase 2: Data Models & Ingestion
- [x] Phase 3: Embedding & Storage
- [x] Phase 4: Retrieval Pipeline
- [x] Phase 5: Generation Module
- [x] Phase 6: Evaluation & API
- [x] Phase 7: Documentation & Commit
- [x] Phase 8: Baseline Comparison Tests
- [x] Phase 9: Fast LLM Tiered Implementation
- [x] Phase 10: Multi-level Chunk + LLM Summary
- [x] Phase 11: Chinese Reranker Optimization
- [x] Phase 12: Project Completion & Finalization
