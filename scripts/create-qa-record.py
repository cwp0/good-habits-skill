#!/usr/bin/env python3
"""create-qa-record.py

在项目根目录的 .good-habits/ 下创建一个 Q&A 记录文件。

用法：
    python3 create-qa-record.py <project_root> \
        [--question "用户问题"] \
        [--solution "实现方案摘要"] \
        [--files "src/a.py: 新增 X / src/b.py: 修复 Y"] \
        [--notes "备注"]

仅传 project_root 时，会生成只含模板占位符的空白文件，由调用方再填充。
脚本最终会把生成文件的绝对路径打印到 stdout，便于上层流程引用。
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

TEMPLATE = """# Q&A 记录 - {timestamp}

> 由 good-habits-skill 自动生成

## 用户问题

{question}

## 实现方案

{solution}

## 修改的文件及内容摘要

{files}

## 备注

{notes}
"""

DEFAULTS = {
    "question": "_（请填写用户原始问题）_",
    "solution": "_（请填写本次实现方案摘要）_",
    "files": "_（请按 `路径: 改动说明` 的格式逐行列出）_",
    "notes": "_（无）_",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Q&A record file under <project_root>/.good-habits/")
    parser.add_argument("project_root", help="项目根目录绝对路径")
    parser.add_argument("--question", default=DEFAULTS["question"], help="用户原始问题")
    parser.add_argument("--solution", default=DEFAULTS["solution"], help="本次实现方案摘要")
    parser.add_argument("--files", default=DEFAULTS["files"], help="修改文件说明，多行用 \\n 分隔")
    parser.add_argument("--notes", default=DEFAULTS["notes"], help="备注")
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.is_dir():
        print(f"Error: project root not found: {project_root}", file=sys.stderr)
        return 1

    qa_dir = project_root / ".good-habits"
    qa_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = qa_dir / f"{timestamp}.md"

    content = TEMPLATE.format(
        timestamp=timestamp,
        question=args.question,
        solution=args.solution,
        files=args.files.replace("\\n", "\n"),
        notes=args.notes,
    )
    file_path.write_text(content, encoding="utf-8")

    print(file_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
