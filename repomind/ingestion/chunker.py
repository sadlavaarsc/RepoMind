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
        Markdown 分块策略：
        1. 文件级 chunk（完整内容）
        2. 按 #/##/### 标题分块
        """
        chunks = []

        # 1. 文件级 chunk
        chunks.append(CodeChunk(
            content=content,
            file_path=file_path,
            function_name=None,
            class_name=None,
            language="markdown",
            chunk_type="file",
            name=Path(file_path).name
        ))

        # 2. 按标题分块
        lines = content.split('\n')
        current_section = []
        current_heading = None

        for line in lines:
            if line.startswith('#'):
                # 保存上一个 section
                if current_section and current_heading:
                    section_content = '\n'.join(current_section)
                    chunks.append(CodeChunk(
                        content=section_content,
                        file_path=file_path,
                        function_name=None,
                        class_name=None,
                        language="markdown",
                        chunk_type="section",
                        name=current_heading
                    ))
                # 开始新 section
                current_heading = line.strip()
                current_section = [line]
            else:
                current_section.append(line)

        # 保存最后一个 section
        if current_section and current_heading:
            section_content = '\n'.join(current_section)
            chunks.append(CodeChunk(
                content=section_content,
                file_path=file_path,
                function_name=None,
                class_name=None,
                language="markdown",
                chunk_type="section",
                name=current_heading
            ))

        return chunks

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
