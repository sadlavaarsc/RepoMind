"""
Parser for extracting structured data from baseline test results.

Parses:
1. comparison_report.md - for answers and performance metrics
2. prompts/query*.md - for retrieved context
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional


def parse_comparison_report(report_path: Path, target_system: Optional[str] = None) -> Dict[int, Dict[str, Any]]:
    """
    Parse comparison_report.md and extract structured data.

    Args:
        report_path: Path to comparison_report.md
        target_system: Optional system name to extract from multi-system reports.
            For multi-system reports (with --- separators between systems),
            specify which system's data to extract. System names should match
            the display names in the report (e.g., "Structured RAG",
            "Full System", "Full System Fast", etc.)

    Returns:
    {
      query_id: {
        "question": str,
        "pred_answer": str,
        "retrieved_files": List[str],
        "latency_ms": float,
        "prompt_tokens": int,
        "completion_tokens": int,
      }
    }
    """
    if not report_path.exists():
        return {}

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    results = {}

    # Split content into query sections
    query_sections = re.split(r"### 查询 \d+ \(ID: (\d+),", content)

    # query_sections[0] is preamble, then pairs of (id, section)
    for i in range(1, len(query_sections), 2):
        if i + 1 >= len(query_sections):
            break

        query_id = int(query_sections[i])
        section = query_sections[i + 1]

        # Extract question
        question_match = re.search(r"\*\*问题\*\*:\s*(.*?)\n", section)
        question = question_match.group(1).strip() if question_match else ""

        if target_system:
            # Multi-system format: extract data for the target system

            # First, extract the performance table and find the target system's row
            perf_match = re.search(
                r"\| 系统 \| Latency \(ms\) \| Prompt Tokens \| Completion Tokens \| Total Tokens \|\n.*?\n((?:\|.*\|\n)+)",
                section,
                re.DOTALL
            )

            latency_ms = 0.0
            prompt_tokens = 0
            completion_tokens = 0

            if perf_match:
                table_rows = perf_match.group(1).strip()
                for row in table_rows.split("\n"):
                    row = row.strip()
                    if not row or row.startswith("|------"):
                        continue
                    # Parse table row: | System Name | latency | prompt | completion | total |
                    cells = [c.strip() for c in row.split("|")[1:-1]]
                    if len(cells) >= 5:
                        sys_name = cells[0]
                        # Match by system name
                        sys_key = sys_name.lower().replace(" ", "_")
                        target_key = target_system.lower().replace(" ", "_")
                        if sys_key == target_key or sys_name == target_system:
                            try:
                                latency_ms = float(cells[1])
                                prompt_tokens = int(cells[2])
                                completion_tokens = int(cells[3])
                            except (ValueError, IndexError):
                                pass
                            break

            # Now extract the answer section for the target system
            # Split into system sections by "---"
            answer_start = section.find("#### 详细答案")
            pred_answer = ""
            retrieved_files = []

            if answer_start != -1:
                answer_section = section[answer_start:]
                # Split by "---" to get individual system answers
                system_parts = re.split(r"\n---\n", answer_section)

                for part in system_parts:
                    # Find the system header anywhere in the part
                    # Look for pattern like "**Structured RAG**:"
                    sys_header_match = re.search(r'^\s*\*\*([^*]+)\*\*:\s*$', part.strip(), re.MULTILINE)

                    if sys_header_match:
                        sys_name = sys_header_match.group(1).strip()
                        sys_key = sys_name.lower().replace(" ", "_")
                        target_key = target_system.lower().replace(" ", "_")

                        if sys_key == target_key or sys_name == target_system:
                            # Extract answer from this section
                            # Find everything after the system header
                            header_pos = part.find(f"**{sys_name}**:")
                            if header_pos != -1:
                                after_header = part[header_pos + len(f"**{sys_name}**:"):]

                                lines = after_header.split("\n")
                                answer_lines = []
                                in_answer = False

                                for line in lines:
                                    line = line.rstrip()
                                    # Skip until we get past any leading empty lines after header
                                    if not in_answer and not line.strip():
                                        continue
                                    in_answer = True

                                    if line.startswith("参考文件：") or line.startswith("**源文件**:"):
                                        break
                                    if line.strip():
                                        answer_lines.append(line)

                                pred_answer = "\n".join(answer_lines).strip()

                            # Extract retrieved files from this section
                            sources_match = re.search(r"\*\*源文件\*\*:(.*?)(?=\n---|\n###|\Z)", part, re.DOTALL)
                            if sources_match:
                                sources_content = sources_match.group(1)
                                for line in sources_content.split("\n"):
                                    line = line.strip()
                                    if line.startswith("- "):
                                        retrieved_files.append(line[2:].strip())
                            break

            results[query_id] = {
                "question": question,
                "pred_answer": pred_answer,
                "retrieved_files": retrieved_files,
                "latency_ms": latency_ms,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }
        else:
            # Original single-system format
            # Extract performance metrics
            perf_match = re.search(
                r"\|.*\| (\d+\.?\d*) \| (\d+) \| (\d+) \| (\d+) \|",
                section
            )
            latency_ms = float(perf_match.group(1)) if perf_match else 0.0
            prompt_tokens = int(perf_match.group(2)) if perf_match else 0
            completion_tokens = int(perf_match.group(3)) if perf_match else 0

            # Extract answer (between "#### 详细答案" and "参考文件：")
            answer_start = section.find("#### 详细答案")
            answer_end = section.find("参考文件：", answer_start) if answer_start != -1 else -1

            pred_answer = ""
            if answer_start != -1:
                if answer_end != -1:
                    answer_section = section[answer_start:answer_end]
                else:
                    answer_section = section[answer_start:]

                # Extract the answer after the system label
                # Skip lines like "**Structured RAG**:"
                lines = answer_section.split("\n")
                answer_lines = []
                in_answer = False
                for line in lines:
                    line = line.rstrip()
                    if line.startswith("**") and line.endswith("**:"):
                        in_answer = True
                        continue
                    if in_answer and line.strip() and not line.startswith("参考文件：") and not line.startswith("**源文件**:"):
                        answer_lines.append(line)
                    if line.startswith("参考文件：") or line.startswith("**源文件**:"):
                        break

                pred_answer = "\n".join(answer_lines).strip()

            # Extract retrieved files (from "**源文件**:" section)
            retrieved_files = []
            sources_match = re.search(r"\*\*源文件\*\*:(.*?)(?=\n---|\n###|\Z)", section, re.DOTALL)
            if sources_match:
                sources_content = sources_match.group(1)
                for line in sources_content.split("\n"):
                    line = line.strip()
                    if line.startswith("- "):
                        retrieved_files.append(line[2:].strip())

            results[query_id] = {
                "question": question,
                "pred_answer": pred_answer,
                "retrieved_files": retrieved_files,
                "latency_ms": latency_ms,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }

    return results


def parse_prompt_file(prompt_path: Path) -> Tuple[str, str]:
    """
    Parse prompt file and extract query and retrieved context.

    Returns:
    (query, retrieved_context)
    - query: the question
    - retrieved_context: all code snippets from "代码上下文：" section
    """
    if not prompt_path.exists():
        return "", ""

    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract query
    query_match = re.search(r"\*\*查询\*\*:\s*(.*?)\n", content)
    query = query_match.group(1).strip() if query_match else ""

    # Extract retrieved context (everything after "代码上下文：")
    context_start = content.find("代码上下文：")
    retrieved_context = ""
    if context_start != -1:
        # Extract from "代码上下文：" to the end (or "请给出你的答案")
        context_end = content.find("请给出你的答案", context_start)
        if context_end != -1:
            retrieved_context = content[context_start:context_end].strip()
        else:
            retrieved_context = content[context_start:].strip()

    return query, retrieved_context


def find_prompt_file(prompts_dir: Path, query_id: int) -> Optional[Path]:
    """
    Find prompt file for a specific query ID.

    Prompt filename pattern: query{id}_*.md
    """
    if not prompts_dir.exists():
        return None

    for prompt_file in prompts_dir.glob("query*.md"):
        # Match query ID at the beginning
        match = re.match(r"query(\d+)_", prompt_file.name)
        if match and int(match.group(1)) == query_id:
            return prompt_file

    return None
