import os
from typing import List, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from repomind.ingestion.models import CodeChunk
from repomind.ingestion.parsers.python_parser import PythonParser


class Chunker:
    """Orchestrate code chunking for multiple languages."""

    def __init__(self, max_workers: int = 4):
        self.parsers = {
            ".py": PythonParser(),
        }
        self.max_workers = max_workers

    def chunk_repository(self, repo_path: str, parallel: bool = True) -> List[CodeChunk]:
        """Chunk an entire repository into code chunks."""
        chunks = []
        repo_path = os.path.abspath(repo_path)

        if not os.path.isdir(repo_path):
            return chunks

        # Collect all files first
        all_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                all_files.append(os.path.join(root, file))

        if parallel and len(all_files) > 1:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.chunk_file, file_path): file_path for file_path in all_files}
                for future in as_completed(futures):
                    try:
                        file_chunks = future.result()
                        chunks.extend(file_chunks)
                    except Exception as e:
                        file_path = futures[future]
                        print(f"Warning: Failed to chunk {file_path}: {e}")
        else:
            # Sequential processing
            for file_path in all_files:
                try:
                    file_chunks = self.chunk_file(file_path)
                    chunks.extend(file_chunks)
                except Exception as e:
                    print(f"Warning: Failed to chunk {file_path}: {e}")

        return chunks

    def chunk_file(self, file_path: str) -> List[CodeChunk]:
        """Chunk a single file into code chunks."""

        # 1. 检查是否应该跳过
        if self._should_skip_file(file_path):
            return []

        ext = os.path.splitext(file_path)[1].lower()

        # 2. 检查是否是文本文件
        if not self._is_text_file(file_path):
            return []

        # 3. 使用专用 parser
        if ext in self.parsers:
            parser = self.parsers[ext]
            return parser.parse_file(file_path)

        # 4. Markdown 特殊处理
        if ext == '.md':
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return self._chunk_markdown(file_path, content)
            except Exception:
                return []

        # 5. 其他文件使用启发式方法
        return self._chunk_file_heuristic(file_path)

    def _should_skip_file(self, file_path: str) -> bool:
        """
        检查是否应该跳过该文件：
        1. 隐藏文件/目录（以 . 开头）
        2. 常见的二进制文件扩展名
        """
        path_obj = Path(file_path)

        # 检查是否在隐藏目录中（如 .git/）
        for part in path_obj.parts:
            if part.startswith('.') and len(part) > 1:  # 不跳过 . 和 ..
                return True

        # 检查文件本身是否是隐藏文件
        if path_obj.name.startswith('.'):
            return True

        # 检查常见的二进制文件扩展名
        binary_exts = {
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',  # 图片（.svg 是文本）
            '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',  # 文档
            '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',  # 压缩包
            '.exe', '.dll', '.so', '.dylib', '.a', '.lib',  # 二进制
            '.pyc', '.pyo', '.class', '.jar', '.war',  # 编译产物
            '.pkl', '.pickle', '.npy', '.npz', '.h5', '.hdf5',  # 数据文件
            '.db', '.sqlite', '.sqlite3',  # 数据库
            '.bin', '.dat', '.idx', '.pack',  # 其他二进制
        }
        if path_obj.suffix.lower() in binary_exts:
            return True

        return False

    def _is_text_file(self, file_path: str, sample_size: int = 1024) -> bool:
        """
        检查文件是否是文本文件：
        1. 检查是否有空字节（二进制文件特征）
        2. 尝试用 UTF-8 解码
        """
        try:
            with open(file_path, 'rb') as f:
                sample = f.read(sample_size)

            # 空文件视为文本文件
            if not sample:
                return True

            # 检查空字节
            if b'\x00' in sample:
                return False

            # 尝试 UTF-8 解码
            try:
                sample.decode('utf-8')
                return True
            except UnicodeDecodeError:
                return False

        except Exception:
            return False

    def _chunk_markdown(self, file_path: str, content: str) -> List[CodeChunk]:
        """
        Markdown 分块策略（改进版）：
        1. 检测代码块边界，避免误识别代码注释
        2. 解析标题层级，自动确定最高级标题
        3. 按最高级+1层级切分（例如最高级是h2则按h3切分，或h1按h2切分）
        4. 自动合并过短的 chunks
        """
        # 配置参数
        MIN_CHUNK_LENGTH = 200  # 最小 chunk 长度（字符）
        MAX_CHUNK_LENGTH = 4000  # 最大 chunk 长度（字符）

        lines = content.split('\n')
        chunks = []

        # Phase 1: 提取结构信息 - 标题位置、代码块边界
        headings, in_code_block = self._extract_markdown_structure(lines)

        if not headings:
            # 没有标题，整个文件作为一个 chunk
            return [CodeChunk(
                content=content,
                file_path=file_path,
                function_name=None,
                class_name=None,
                language="markdown",
                chunk_type="file",
                name=Path(file_path).name
            )]

        # Phase 2: 确定切分层级 - 找到最高级标题，然后切分下一级
        min_level = min(h[1] for h in headings)
        split_level = min_level + 1  # 最高级是 h1 则按 h2 切分，最高级是 h2 则按 h3 切分

        # Phase 3: 生成初始 chunks
        initial_chunks = self._create_chunks_by_level(
            lines, headings, split_level, min_level, file_path
        )

        # Phase 4: 合并短 chunks
        merged_chunks = self._merge_short_chunks(
            initial_chunks, MIN_CHUNK_LENGTH, MAX_CHUNK_LENGTH
        )

        return merged_chunks

    def _extract_markdown_structure(self, lines):
        """
        Phase 1: 提取 Markdown 结构信息
        返回: (headings, in_code_block)
          - headings: [(line_idx, level, text), ...]
          - in_code_block: [bool, ...] 表示每行是否在代码块内
        """
        headings = []
        in_code_block = [False] * len(lines)
        code_block_state = False

        for i, line in enumerate(lines):
            in_code_block[i] = code_block_state

            # 检测代码块边界
            stripped = line.strip()
            if stripped.startswith('```'):
                code_block_state = not code_block_state
                continue

            # 在代码块内，不检测标题
            if code_block_state:
                continue

            # 检测标题
            if line.startswith('#'):
                # 计算标题层级
                level = 0
                while level < len(line) and line[level] == '#':
                    level += 1
                # 确保 # 后面有空格或标题结束
                if level < len(line) and (line[level] == ' ' or line[level] == '\t'):
                    heading_text = line.strip()
                    headings.append((i, level, heading_text))

        return headings, in_code_block

    def _create_chunks_by_level(self, lines, headings, split_level, min_level, file_path):
        """
        Phase 3: 按指定层级创建 chunks
        策略：
        - 如果有 split_level 的标题，按 split_level 切分
        - 如果没有 split_level 的标题，按 min_level 切分
        - 每个 chunk 包含标题及其所有子内容
        """
        chunks = []

        # 确定实际使用的切分层级
        split_headings = [h for h in headings if h[1] == split_level]
        if not split_headings:
            split_headings = [h for h in headings if h[1] == min_level]

        if not split_headings:
            # 没有找到切分用的标题，返回整个文件
            return [CodeChunk(
                content='\n'.join(lines),
                file_path=file_path,
                function_name=None,
                class_name=None,
                language="markdown",
                chunk_type="file",
                name=Path(file_path).name
            )]

        # 为每个切分标题确定内容范围
        for i, (start_line, level, heading_text) in enumerate(split_headings):
            # 找到下一个同级或更高级标题的位置
            end_line = len(lines)
            for j in range(i + 1, len(split_headings)):
                next_start = split_headings[j][0]
                if next_start > start_line:
                    end_line = next_start
                    break

            # 还需要检查是否有更高级的标题在中间
            for h in headings:
                h_line, h_level, _ = h
                if h_line > start_line and h_line < end_line and h_level <= level:
                    end_line = h_line
                    break

            # 提取内容
            chunk_lines = lines[start_line:end_line]
            chunk_content = '\n'.join(chunk_lines)

            chunks.append(CodeChunk(
                content=chunk_content,
                file_path=file_path,
                function_name=None,
                class_name=None,
                language="markdown",
                chunk_type="section",
                name=heading_text
            ))

        # 检查开头是否有前置内容（在第一个切分标题之前）
        first_split_line = split_headings[0][0]
        if first_split_line > 0:
            prefix_content = '\n'.join(lines[:first_split_line]).strip()
            if prefix_content:
                chunks.insert(0, CodeChunk(
                    content='\n'.join(lines[:first_split_line]),
                    file_path=file_path,
                    function_name=None,
                    class_name=None,
                    language="markdown",
                    chunk_type="section",
                    name="前置内容"
                ))

        return chunks

    def _merge_short_chunks(self, chunks, min_length, max_length):
        """
        Phase 4: 合并过短的 chunks
        策略：
        - 从前往后扫描，遇到短 chunk 时尝试与后面的合并
        - 优先合并同一层级的
        - 不超过最大长度限制
        """
        if len(chunks) <= 1:
            return chunks

        merged = []
        current_chunk = None

        for chunk in chunks:
            if current_chunk is None:
                current_chunk = chunk
            else:
                current_len = len(current_chunk.content)
                new_len = len(chunk.content)

                # 如果当前 chunk 太短，尝试合并
                if current_len < min_length and (current_len + new_len) <= max_length:
                    # 合并
                    merged_content = current_chunk.content + '\n' + chunk.content
                    merged_name = current_chunk.name
                    if chunk.name != "前置内容":
                        merged_name = merged_name + " + " + chunk.name

                    current_chunk = CodeChunk(
                        content=merged_content,
                        file_path=chunk.file_path,
                        function_name=chunk.function_name,
                        class_name=chunk.class_name,
                        language=chunk.language,
                        chunk_type=chunk.chunk_type,
                        name=merged_name
                    )
                else:
                    # 当前 chunk 足够长，或者合并后太长
                    merged.append(current_chunk)
                    current_chunk = chunk

        if current_chunk is not None:
            merged.append(current_chunk)

        return merged

    def _chunk_file_heuristic(self, file_path: str) -> List[CodeChunk]:
        """Simple heuristic chunking for unsupported languages."""
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return []

        language = self._guess_language(file_path)
        return [CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language=language
        )]

    def _guess_language(self, file_path: str) -> str:
        """Guess programming language from file extension."""
        ext_map = {
            # 编程语言
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".sh": "shell",
            ".bash": "shell",
            ".zsh": "shell",
            # 配置文件
            ".yaml": "yaml",
            ".yml": "yaml",
            ".json": "json",
            ".xml": "xml",
            ".toml": "toml",
            ".ini": "ini",
            ".cfg": "config",
            ".conf": "config",
            # 文档
            ".md": "markdown",
            ".rst": "restructuredtext",
            ".txt": "text",
            # Web
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".scss": "scss",
            ".sass": "sass",
            ".less": "less",
            ".svg": "svg",
            # 数据
            ".csv": "csv",
            ".tsv": "tsv",
        }
        ext = os.path.splitext(file_path)[1].lower()
        return ext_map.get(ext, "unknown")
