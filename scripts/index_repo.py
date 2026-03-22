#!/usr/bin/env python
"""CLI script to index a repository."""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from repomind.configs.settings import get_settings
from repomind.ingestion.chunker import Chunker
from repomind.indexing.embedding_service import EmbeddingService
from repomind.indexing.index_builder import IndexBuilder
from repomind.storage.faiss_store import FAISSStore


def main():
    parser = argparse.ArgumentParser(description="Index a code repository")
    parser.add_argument("repo_path", help="Path to the repository to index")
    parser.add_argument("--output", "-o", help="Path to save the index (optional)")

    args = parser.parse_args()

    settings = get_settings()

    print(f"Indexing repository: {args.repo_path}")

    embedding_service = EmbeddingService(
        api_key=settings.qwen_api_key,
        base_url=settings.base_url,
        model=settings.embedding_model
    )

    chunker = Chunker()
    vector_store = FAISSStore(embedding_service=embedding_service)
    index_builder = IndexBuilder(chunker, vector_store, embedding_service)

    print("Parsing and chunking files...")
    index_builder.build_index(args.repo_path)

    num_chunks = len(vector_store.chunks)
    print(f"Indexed {num_chunks} chunks")

    output_path = args.output or settings.vector_store_path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    index_builder.save_index(output_path)
    print(f"Index saved to: {output_path}")


if __name__ == "__main__":
    main()
