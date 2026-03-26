from typing import List, Tuple, Set, Optional
from pathlib import Path
from repomind.ingestion.models import CodeChunk


class Reranker:
    """
    Balanced Reranker with Bucket Guarantee and MMR Diversity.

    Ensures:
    - At least 1 document chunk (README, docs, etc.)
    - At least 1 code chunk
    - Diversity via MMR (Maximal Marginal Relevance)
    - Minor bias towards document chunks
    """

    # 中文无意义代词排除表
    CHINESE_STOPWORDS = {
        "我", "我们", "你", "你们", "他", "他们",
        "她", "她们", "它", "它们", "这", "那",
        "这个", "那个", "这些", "那些", "是", "的",
        "了", "吗", "呢", "吧", "啊", "呀",
        "和", "或", "但", "而", "因为", "所以",
        "什么", "怎么", "如何", "为什么", "哪", "哪里",
    }

    # Keyword scoring constants
    KEYWORD_FILE_PATH_BOOST = 0.3
    KEYWORD_FUNC_NAME_MATCH = 0.25
    KEYWORD_FUNC_NAME_CONTAINS = 0.25
    KEYWORD_CLASS_NAME_MATCH = 0.25
    KEYWORD_CLASS_NAME_CONTAINS = 0.25
    KEYWORD_BIGRAM_MATCH_PER = 0.04
    KEYWORD_BIGRAM_MAX = 0.2
    KEYWORD_TRIGRAM_MATCH_PER = 0.05
    KEYWORD_TRIGRAM_MAX = 0.2
    KEYWORD_ENGLISH_WORD_MATCH_PER = 0.1
    KEYWORD_ENGLISH_MAX = 0.4
    KEYWORD_MAX_SCORE = 1.0

    def __init__(
        self,
        alpha: float = 0.85,
        beta: float = 0.15,
        lambda_: float = 0.75,
        doc_bias: float = 0.05,
        min_doc_count: int = 1,
        min_code_count: int = 1,
        embedding_service=None,
    ):
        self.alpha = alpha
        self.beta = beta
        self.lambda_ = lambda_
        self.doc_bias = doc_bias
        self.min_doc_count = min_doc_count
        self.min_code_count = min_code_count
        self.embedding_service = embedding_service

    def rerank(
        self,
        chunks_with_scores: List[Tuple[CodeChunk, float]],
        query: str
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Rerank chunks with bucket guarantee and MMR diversity.

        Args:
            chunks_with_scores: List of (chunk, embedding_score) tuples.
            query: Original user query.

        Returns:
            Reranked list of (chunk, combined_score) tuples.
        """
        if not chunks_with_scores:
            return []

        # Step 1: Split into buckets
        doc_candidates, code_candidates = self._split_buckets(chunks_with_scores)

        # Step 2: Calculate keyword scores for all candidates
        query_lower = query.lower()
        doc_with_keyword = [
            (chunk, emb_score, self._calculate_keyword_score(chunk, query_lower))
            for chunk, emb_score in doc_candidates
        ]
        code_with_keyword = [
            (chunk, emb_score, self._calculate_keyword_score(chunk, query_lower))
            for chunk, emb_score in code_candidates
        ]

        # Step 3: Combine scores (embedding + keyword + doc bias)
        doc_scored = self._combine_scores(doc_with_keyword, is_doc=True)
        code_scored = self._combine_scores(code_with_keyword, is_doc=False)

        # Step 4: Select with bucket guarantee and MMR
        selected = self._select_with_guarantee(doc_scored, code_scored)

        # Step 5: Final MMR rerank for global optimization
        if len(selected) > 1:
            selected = self._mmr_select(selected, query, k=len(selected), lambda_=self.lambda_)

        return selected

    def _split_buckets(
        self,
        chunks_with_scores: List[Tuple[CodeChunk, float]]
    ) -> Tuple[List[Tuple[CodeChunk, float]], List[Tuple[CodeChunk, float]]]:
        """Split chunks into document and code buckets."""
        doc_bucket = []
        code_bucket = []

        for chunk, score in chunks_with_scores:
            if self._is_doc_chunk(chunk):
                doc_bucket.append((chunk, score))
            else:
                code_bucket.append((chunk, score))

        return doc_bucket, code_bucket

    def _is_doc_chunk(self, chunk: CodeChunk) -> bool:
        """Check if a chunk is a document (README, markdown, etc.)."""
        path_lower = chunk.file_path.lower()
        return path_lower.endswith((".md", ".rst", ".txt"))

    def _calculate_keyword_score(self, chunk: CodeChunk, query_lower: str) -> float:
        """Calculate keyword overlap score between chunk and query."""
        score = 0.0

        file_path_lower = chunk.file_path.lower()

        if query_lower in file_path_lower:
            score += self.KEYWORD_FILE_PATH_BOOST

        if chunk.function_name:
            func_name_lower = chunk.function_name.lower()
            if func_name_lower in query_lower:
                score += self.KEYWORD_FUNC_NAME_MATCH
            if query_lower in func_name_lower:
                score += self.KEYWORD_FUNC_NAME_CONTAINS

        if chunk.class_name:
            class_name_lower = chunk.class_name.lower()
            if class_name_lower in query_lower:
                score += self.KEYWORD_CLASS_NAME_MATCH
            if query_lower in class_name_lower:
                score += self.KEYWORD_CLASS_NAME_CONTAINS

        content_lower = chunk.content.lower()

        # 检测是否为中文查询
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in query_lower)

        if has_chinese:
            # 中文：同时使用 2-gram 和 3-gram 匹配
            def get_ngrams(text, n):
                text = text.replace(" ", "").replace("\n", "")
                return [text[i:i+n] for i in range(len(text)-n+1)]

            # 2-gram 匹配
            query_bigrams = set(get_ngrams(query_lower, 2))
            # 过滤无意义的 2-gram
            query_bigrams = {
                bg for bg in query_bigrams
                if not any(stop in bg for stop in self.CHINESE_STOPWORDS)
            }
            if query_bigrams:
                content_bigrams = get_ngrams(content_lower, 2)
                bigram_matches = sum(1 for bg in content_bigrams if bg in query_bigrams)
                if bigram_matches > 0:
                    score += min(self.KEYWORD_BIGRAM_MAX, bigram_matches * self.KEYWORD_BIGRAM_MATCH_PER)

            # 3-gram 匹配
            query_trigrams = set(get_ngrams(query_lower, 3))
            # 过滤无意义的 3-gram
            query_trigrams = {
                tg for tg in query_trigrams
                if not any(stop in tg for stop in self.CHINESE_STOPWORDS)
            }
            if query_trigrams:
                content_trigrams = get_ngrams(content_lower, 3)
                trigram_matches = sum(1 for tg in content_trigrams if tg in query_trigrams)
                if trigram_matches > 0:
                    score += min(self.KEYWORD_TRIGRAM_MAX, trigram_matches * self.KEYWORD_TRIGRAM_MATCH_PER)
        else:
            # 英文：保持原有逻辑
            query_words = [word for word in query_lower.split() if len(word) > 2]

            if query_words:
                matches = sum(1 for word in query_words if word in content_lower)
                score += min(self.KEYWORD_ENGLISH_MAX, matches * self.KEYWORD_ENGLISH_WORD_MATCH_PER)

        return min(self.KEYWORD_MAX_SCORE, score)

    def _combine_scores(
        self,
        candidates: List[Tuple[CodeChunk, float, float]],
        is_doc: bool
    ) -> List[Tuple[CodeChunk, float]]:
        """Combine embedding score and keyword score, with optional doc bias."""
        combined = []
        for chunk, emb_score, keyword_score in candidates:
            base_score = self.alpha * emb_score + self.beta * keyword_score
            if is_doc:
                base_score += self.doc_bias
            combined.append((chunk, base_score))
        return combined

    def _select_with_guarantee(
        self,
        doc_scored: List[Tuple[CodeChunk, float]],
        code_scored: List[Tuple[CodeChunk, float]],
        final_k: int = 5
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Select chunks with bucket guarantees and MMR diversity.

        Guarantees:
        - At least min_doc_count document chunks
        - At least min_code_count code chunks
        - No duplicate files
        - Diversity via MMR
        """
        selected: List[Tuple[CodeChunk, float]] = []
        seen_files: Set[str] = set()

        # Sort by score descending
        doc_sorted = sorted(doc_scored, key=lambda x: x[1], reverse=True)
        code_sorted = sorted(code_scored, key=lambda x: x[1], reverse=True)

        # Step 1: Guarantee minimum doc chunks
        selected, seen_files = self._guarantee_docs(
            doc_sorted, selected, seen_files
        )

        # Step 2: Guarantee minimum code chunks
        selected, seen_files = self._guarantee_code(
            code_sorted, selected, seen_files
        )

        # Step 3: Fill remaining slots
        selected = self._fill_remaining_slots(
            doc_sorted, code_sorted, selected, seen_files, final_k
        )

        return selected

    def _guarantee_docs(
        self,
        doc_sorted: List[Tuple[CodeChunk, float]],
        selected: List[Tuple[CodeChunk, float]],
        seen_files: Set[str]
    ) -> Tuple[List[Tuple[CodeChunk, float]], Set[str]]:
        """Guarantee minimum document chunks with MMR diversity."""
        doc_guaranteed = 0
        doc_remaining = doc_sorted.copy()

        while doc_guaranteed < self.min_doc_count and doc_remaining:
            if doc_guaranteed == 0:
                chunk, score = doc_remaining[0]
            else:
                mmr_selection = self._mmr_select(
                    [(c, s) for c, s in doc_remaining if self._get_file_key(c) not in seen_files],
                    query="",
                    k=1,
                    lambda_=self.lambda_,
                    already_selected=selected
                )
                if not mmr_selection:
                    break
                chunk, score = mmr_selection[0]

            file_key = self._get_file_key(chunk)
            if file_key not in seen_files:
                selected.append((chunk, score))
                seen_files.add(file_key)
                doc_guaranteed += 1
                doc_remaining = [(c, s) for c, s in doc_remaining if c is not chunk]

        return selected, seen_files

    def _guarantee_code(
        self,
        code_sorted: List[Tuple[CodeChunk, float]],
        selected: List[Tuple[CodeChunk, float]],
        seen_files: Set[str]
    ) -> Tuple[List[Tuple[CodeChunk, float]], Set[str]]:
        """Guarantee minimum code chunks with MMR diversity."""
        code_guaranteed = 0
        code_remaining = code_sorted.copy()

        while code_guaranteed < self.min_code_count and code_remaining:
            if code_guaranteed == 0:
                chunk, score = code_remaining[0]
            else:
                mmr_selection = self._mmr_select(
                    [(c, s) for c, s in code_remaining if self._get_file_key(c) not in seen_files],
                    query="",
                    k=1,
                    lambda_=self.lambda_,
                    already_selected=selected
                )
                if not mmr_selection:
                    break
                chunk, score = mmr_selection[0]

            file_key = self._get_file_key(chunk)
            if file_key not in seen_files:
                selected.append((chunk, score))
                seen_files.add(file_key)
                code_guaranteed += 1
                code_remaining = [(c, s) for c, s in code_remaining if c is not chunk]

        return selected, seen_files

    def _fill_remaining_slots(
        self,
        doc_sorted: List[Tuple[CodeChunk, float]],
        code_sorted: List[Tuple[CodeChunk, float]],
        selected: List[Tuple[CodeChunk, float]],
        seen_files: Set[str],
        final_k: int
    ) -> List[Tuple[CodeChunk, float]]:
        """Fill remaining slots with MMR for diversity."""
        remaining: List[Tuple[CodeChunk, float]] = []
        for chunk, score in doc_sorted:
            file_key = self._get_file_key(chunk)
            if file_key not in seen_files:
                remaining.append((chunk, score))
        for chunk, score in code_sorted:
            file_key = self._get_file_key(chunk)
            if file_key not in seen_files:
                remaining.append((chunk, score))

        remaining_slots = final_k - len(selected)
        if remaining_slots > 0 and remaining:
            mmr_selected = self._mmr_select(
                remaining,
                query="",
                k=remaining_slots,
                lambda_=self.lambda_,
                already_selected=selected
            )
            for chunk, score in mmr_selected:
                file_key = self._get_file_key(chunk)
                if file_key not in seen_files:
                    selected.append((chunk, score))
                    seen_files.add(file_key)

        return selected

    def _mmr_select(
        self,
        candidates: List[Tuple[CodeChunk, float]],
        query: str,
        k: int,
        lambda_: float,
        already_selected: List[Tuple[CodeChunk, float]] = None
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Select chunks using MMR (Maximal Marginal Relevance) for diversity.

        MMR formula:
        MMR = λ * Relevance(chunk, query) - (1-λ) * max_{s∈selected} Similarity(chunk, s)

        Args:
            candidates: List of (chunk, relevance_score) tuples
            query: Original query (for relevance)
            k: Number of chunks to select
            lambda_: Tradeoff between relevance and diversity (0.0-1.0)
            already_selected: Already selected chunks for diversity calculation

        Returns:
            List of selected (chunk, score) tuples
        """
        if not candidates:
            return []

        selected: List[Tuple[CodeChunk, float]] = []
        if already_selected:
            selected = already_selected.copy()

        remaining = candidates.copy()

        while len(selected) < len(already_selected if already_selected else []) + k and remaining:
            best_chunk = None
            best_score = -float("inf")

            for chunk, rel_score in remaining:
                relevance = rel_score

                max_sim = 0.0
                if selected:
                    max_sim = max(
                        self._calculate_chunk_similarity(chunk, s_chunk)
                        for s_chunk, _ in selected
                    )

                mmr_score = lambda_ * relevance - (1 - lambda_) * max_sim

                if mmr_score > best_score:
                    best_score = mmr_score
                    best_chunk = (chunk, rel_score)

            if best_chunk:
                selected.append(best_chunk)
                remaining = [(c, s) for c, s in remaining if c is not best_chunk[0]]
            else:
                break

        if already_selected:
            return selected[len(already_selected):]
        return selected[:k]

    def _calculate_chunk_similarity(
        self,
        chunk1: CodeChunk,
        chunk2: CodeChunk
    ) -> float:
        """
        Calculate similarity between two chunks.

        Uses:
        - Semantic similarity via embeddings (if embedding_service available)
        - Fallback to text overlap (backward compatibility)
        """
        if self.embedding_service:
            try:
                text1 = chunk1.get_embedding_text()
                text2 = chunk2.get_embedding_text()

                embeddings = self.embedding_service.embed_batch([text1, text2])
                emb1 = embeddings[0]
                emb2 = embeddings[1]

                return self._cosine_similarity(emb1, emb2)
            except Exception:
                pass

        return self._text_overlap_similarity(chunk1, chunk2)

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _text_overlap_similarity(self, chunk1: CodeChunk, chunk2: CodeChunk) -> float:
        """Simple text overlap similarity (fallback when no embeddings)."""
        if self._get_file_key(chunk1) == self._get_file_key(chunk2):
            return 1.0

        names1 = set()
        if chunk1.function_name:
            names1.add(chunk1.function_name.lower())
        if chunk1.class_name:
            names1.add(chunk1.class_name.lower())

        names2 = set()
        if chunk2.function_name:
            names2.add(chunk2.function_name.lower())
        if chunk2.class_name:
            names2.add(chunk2.class_name.lower())

        if names1 and names2:
            name_overlap = len(names1 & names2) / len(names1 | names2)
            if name_overlap > 0:
                return 0.5 + 0.5 * name_overlap

        content1 = chunk1.content.lower()
        content2 = chunk2.content.lower()
        words1 = set(content1.split())
        words2 = set(content2.split())

        if not words1 or not words2:
            return 0.0

        overlap = len(words1 & words2)
        union = len(words1 | words2)

        if union == 0:
            return 0.0

        return overlap / union

    def _get_file_key(self, chunk: CodeChunk) -> str:
        """Get unique key for a file (to avoid duplicates)."""
        return str(Path(chunk.file_path).resolve())
