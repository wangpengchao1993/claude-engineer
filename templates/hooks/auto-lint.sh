#!/bin/bash
# auto-lint.sh — Automatically lint files after Claude edits them
# auto-lint.sh — 在 Claude 编辑文件后自动进行代码检查
# Usage: Add to .claude/settings.json PostToolUse hooks
# 用法：添加到 .claude/settings.json 的 PostToolUse 钩子中
#
# Configuration:
# 配置示例：
# {
#   "hooks": {
#     "PostToolUse": [{
#       "matcher": "Edit|Write",
#       "hooks": ["./scripts/auto-lint.sh $CLAUDE_FILE_PATH"]
#     }]
#   }
# }

FILE="$1"

# If no file provided or file doesn't exist, exit silently
# 如果未提供文件或文件不存在，静默退出
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    exit 0
fi

# Extract file extension
# 提取文件扩展名
EXT="${FILE##*.}"

case "$EXT" in
    ts|tsx|js|jsx|mjs|cjs)
        # TypeScript / JavaScript
        # TypeScript / JavaScript 代码检查
        if command -v npx &>/dev/null; then
            npx eslint --fix "$FILE" 2>/dev/null
            npx prettier --write "$FILE" 2>/dev/null
        fi
        ;;
    py)
        # Python
        # Python 代码检查
        if command -v ruff &>/dev/null; then
            ruff check --fix "$FILE" 2>/dev/null
            ruff format "$FILE" 2>/dev/null
        elif command -v black &>/dev/null; then
            black "$FILE" 2>/dev/null
        fi
        ;;
    rs)
        # Rust
        # Rust 代码格式化
        if command -v rustfmt &>/dev/null; then
            rustfmt "$FILE" 2>/dev/null
        fi
        ;;
    go)
        # Go
        # Go 代码格式化
        if command -v gofmt &>/dev/null; then
            gofmt -w "$FILE" 2>/dev/null
        fi
        ;;
    json)
        # JSON
        # JSON 格式化
        if command -v npx &>/dev/null; then
            npx prettier --write "$FILE" 2>/dev/null
        elif command -v python3 &>/dev/null; then
            python3 -m json.tool "$FILE" > "${FILE}.tmp" && mv "${FILE}.tmp" "$FILE" 2>/dev/null
        fi
        ;;
    yaml|yml)
        # YAML
        # YAML 格式化
        if command -v npx &>/dev/null; then
            npx prettier --write "$FILE" 2>/dev/null
        fi
        ;;
esac

exit 0
