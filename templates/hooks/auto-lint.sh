#!/bin/bash
# auto-lint.sh — Automatically lint files after Claude edits them
# Usage: Add to .claude/settings.json PostToolUse hooks
#
# Configuration:
# {
#   "hooks": {
#     "PostToolUse": [{
#       "matcher": "Edit|Write",
#       "hooks": ["./scripts/auto-lint.sh $CLAUDE_FILE_PATH"]
#     }]
#   }
# }

FILE="$1"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    exit 0
fi

EXT="${FILE##*.}"

case "$EXT" in
    ts|tsx|js|jsx|mjs|cjs)
        # TypeScript / JavaScript
        if command -v npx &>/dev/null; then
            npx eslint --fix "$FILE" 2>/dev/null
            npx prettier --write "$FILE" 2>/dev/null
        fi
        ;;
    py)
        # Python
        if command -v ruff &>/dev/null; then
            ruff check --fix "$FILE" 2>/dev/null
            ruff format "$FILE" 2>/dev/null
        elif command -v black &>/dev/null; then
            black "$FILE" 2>/dev/null
        fi
        ;;
    rs)
        # Rust
        if command -v rustfmt &>/dev/null; then
            rustfmt "$FILE" 2>/dev/null
        fi
        ;;
    go)
        # Go
        if command -v gofmt &>/dev/null; then
            gofmt -w "$FILE" 2>/dev/null
        fi
        ;;
    json)
        # JSON
        if command -v npx &>/dev/null; then
            npx prettier --write "$FILE" 2>/dev/null
        elif command -v python3 &>/dev/null; then
            python3 -m json.tool "$FILE" > "${FILE}.tmp" && mv "${FILE}.tmp" "$FILE" 2>/dev/null
        fi
        ;;
    yaml|yml)
        # YAML
        if command -v npx &>/dev/null; then
            npx prettier --write "$FILE" 2>/dev/null
        fi
        ;;
esac

exit 0
