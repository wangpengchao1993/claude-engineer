#!/bin/bash
# check-protected-files.sh — Block Claude from editing protected files
# Usage: Add to .claude/settings.json PreToolUse hooks
#
# Configuration:
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

for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$FILE" == *"$pattern"* ]]; then
        echo "BLOCKED: '$FILE' matches protected pattern '$pattern'."
        echo "This file should not be modified directly."
        exit 1
    fi
done

exit 0
