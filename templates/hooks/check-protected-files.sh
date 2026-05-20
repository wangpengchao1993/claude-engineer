#!/bin/bash
# check-protected-files.sh — Block Claude from editing protected files
# check-protected-files.sh — 阻止 Claude 编辑受保护的文件
# Usage: Add to .claude/settings.json PreToolUse hooks
# 用法：添加到 .claude/settings.json 的 PreToolUse 钩子中
#
# Configuration:
# 配置示例：
# {
#   "hooks": {
#     "PreToolUse": [{
#       "matcher": "Edit|Write",
#       "hooks": ["./scripts/check-protected-files.sh $CLAUDE_FILE_PATH"]
#     }]
#   }
# }

FILE="$1"

if [ -z "$FILE" ]; then
    exit 0
fi

# Add patterns for files that should not be modified
# 添加不允许修改的文件匹配模式
PROTECTED_PATTERNS=(
    "migrations/versions/"
    "generated/"
    ".env.production"
    ".env.local"
    "package-lock.json"
    "pnpm-lock.yaml"
    "yarn.lock"
    "Cargo.lock"
    "poetry.lock"
    "vendor/"
    "dist/"
    "node_modules/"
    ".git/"
)

# Loop through each pattern and check if the file matches
# 遍历每个模式，检查文件路径是否匹配
for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$FILE" == *"$pattern"* ]]; then
        echo "BLOCKED: '$FILE' matches protected pattern '$pattern'."
        echo "This file should not be modified directly."
        exit 1
    fi
done

exit 0
