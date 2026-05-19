#!/usr/bin/env bash
# create-qa-record.sh
# 用途：在项目根目录的 .good-habits/ 下创建一个 Q&A 记录文件。
# 用法：
#   ./create-qa-record.sh <project_root> [user_question] [solution_summary] [files_changed] [notes]
# 示例：
#   ./create-qa-record.sh /path/to/project "增加登录功能" "JWT + Redis 缓存" "src/auth.ts: 新增登录接口" "需在生产环境配置 JWT_SECRET"
#
# 仅传 project_root 时，会生成只含模板占位符的空白文件，由调用方再填充。

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project_root> [user_question] [solution_summary] [files_changed] [notes]" >&2
  exit 1
fi

PROJECT_ROOT="$1"
USER_QUESTION="${2:-_（请填写用户原始问题）_}"
SOLUTION_SUMMARY="${3:-_（请填写本次实现方案摘要）_}"
FILES_CHANGED="${4:-_（请按 \`路径: 改动说明\` 的格式逐行列出）_}"
NOTES="${5:-_（无）_}"

if [[ ! -d "$PROJECT_ROOT" ]]; then
  echo "Error: project root not found: $PROJECT_ROOT" >&2
  exit 1
fi

QA_DIR="$PROJECT_ROOT/.good-habits"
mkdir -p "$QA_DIR"

TIMESTAMP="$(date +"%Y-%m-%d-%H-%M-%S")"
FILE_PATH="$QA_DIR/$TIMESTAMP.md"

cat > "$FILE_PATH" <<EOF
# Q&A 记录 - $TIMESTAMP

> 由 good-habits-skill 自动生成

## 用户问题

$USER_QUESTION

## 实现方案

$SOLUTION_SUMMARY

## 修改的文件及内容摘要

$FILES_CHANGED

## 备注

$NOTES
EOF

echo "$FILE_PATH"
