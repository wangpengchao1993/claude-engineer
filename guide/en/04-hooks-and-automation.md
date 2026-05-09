# Hooks & Automation

> Automate your Claude Code workflows with hooks — run shell commands on Claude events, enforce standards, and build custom pipelines.

## Table of Contents

- [What Are Hooks?](#what-are-hooks)
- [Hook Events](#hook-events)
- [Configuration](#configuration)
- [Practical Examples](#practical-examples)
- [Hook Environment Variables](#hook-environment-variables)
- [Advanced Patterns](#advanced-patterns)
- [Non-Interactive Automation](#non-interactive-automation)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## What Are Hooks?

Hooks are shell commands that run automatically when specific Claude Code events occur. They let you:

- **Auto-lint** files after Claude edits them
- **Run tests** after code changes
- **Log prompts** for auditing
- **Send notifications** when Claude finishes
- **Validate** changes before they're applied
- **Enforce** project-specific rules

Hooks are configured in `.claude/settings.json` (project) or `~/.claude/settings.json` (global).

---

## Hook Events

| Event | When It Fires | Common Use Cases |
|-------|---------------|------------------|
| `PreToolUse` | Before Claude calls a tool | Validate, block, or modify tool calls |
| `PostToolUse` | After a tool call completes | Auto-lint, auto-test, log changes |
| `UserPromptSubmit` | When user sends a message | Add context, log prompts |
| `Stop` | When Claude finishes responding | Notifications, final checks |

### Event Flow

```
User sends message
    │
    ├─► [UserPromptSubmit hooks run]
    │
    ▼
Claude processes and decides to use a tool
    │
    ├─► [PreToolUse hooks run]
    │       │
    │       ├─ Hook blocks → tool is skipped
    │       └─ Hook passes → tool executes
    │
    ├─► Tool executes (Edit, Bash, etc.)
    │
    ├─► [PostToolUse hooks run]
    │
    ▼
Claude finishes responding
    │
    └─► [Stop hooks run]
```

---

## Configuration

### Basic Structure

In `.claude/settings.json`:

```jsonc
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName",   // Which tool(s) trigger this hook
        "hooks": [
          "command to run"       // Shell command(s) to execute
        ]
      }
    ]
  }
}
```

### Matcher Patterns

- `""` — Match all tools / all events
- `"Edit"` — Match the Edit tool only
- `"Edit|Write"` — Match Edit or Write
- `"Bash"` — Match any Bash command
- `"Bash(npm test)"` — Match specific Bash command

---

## Practical Examples

### 1. Auto-Lint After Edits

Automatically run your linter whenever Claude edits a file:

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          "npx eslint --fix $CLAUDE_FILE_PATH 2>/dev/null || true"
        ]
      }
    ]
  }
}
```

**Python version:**

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          "ruff check --fix $CLAUDE_FILE_PATH 2>/dev/null; ruff format $CLAUDE_FILE_PATH 2>/dev/null || true"
        ]
      }
    ]
  }
}
```

### 2. Auto-Format After Edits

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          "prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true"
        ]
      }
    ]
  }
}
```

### 3. Run Tests After Code Changes

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          "./scripts/run-related-tests.sh $CLAUDE_FILE_PATH"
        ]
      }
    ]
  }
}
```

`scripts/run-related-tests.sh`:
```bash
#!/bin/bash
# Find and run tests related to the changed file
FILE="$1"
TEST_FILE="${FILE/src\//tests/}"
TEST_FILE="${TEST_FILE%.ts}.test.ts"

if [ -f "$TEST_FILE" ]; then
    npx jest "$TEST_FILE" --no-coverage 2>&1 | tail -5
fi
```

### 4. Prevent Editing Protected Files

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          "./scripts/check-protected.sh $CLAUDE_FILE_PATH"
        ]
      }
    ]
  }
}
```

`scripts/check-protected.sh`:
```bash
#!/bin/bash
PROTECTED_PATTERNS=(
    "migrations/versions/"
    "generated/"
    ".env.production"
    "package-lock.json"
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if [[ "$1" == *"$pattern"* ]]; then
        echo "BLOCKED: $1 is a protected file and should not be modified."
        exit 1
    fi
done
```

### 5. Desktop Notification When Done

```jsonc
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          "notify-send 'Claude Code' 'Task completed!' 2>/dev/null || osascript -e 'display notification \"Task completed!\" with title \"Claude Code\"' 2>/dev/null || true"
        ]
      }
    ]
  }
}
```

### 6. Log All Prompts

```jsonc
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          "echo \"$(date -Iseconds) | $CLAUDE_PROMPT\" >> .claude/prompt-log.txt"
        ]
      }
    ]
  }
}
```

### 7. Add Context to Every Prompt

```jsonc
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          "echo 'Current git branch: '$(git branch --show-current)'; Last commit: '$(git log --oneline -1)"
        ]
      }
    ]
  }
}
```

---

## Hook Environment Variables

Hooks receive context through environment variables:

| Variable | Available In | Description |
|----------|-------------|-------------|
| `$CLAUDE_FILE_PATH` | PreToolUse, PostToolUse | Path of the file being edited |
| `$CLAUDE_TOOL_NAME` | PreToolUse, PostToolUse | Name of the tool being called |
| `$CLAUDE_PROMPT` | UserPromptSubmit | The user's prompt text |

### Blocking a Tool Call

If a `PreToolUse` hook exits with a **non-zero exit code**, the tool call is blocked and Claude sees the hook's output as feedback.

```bash
#!/bin/bash
# Block if file is too large to edit safely
FILE="$1"
if [ -f "$FILE" ]; then
    LINES=$(wc -l < "$FILE")
    if [ "$LINES" -gt 5000 ]; then
        echo "BLOCKED: File has $LINES lines. Consider breaking it up first."
        exit 1
    fi
fi
```

---

## Advanced Patterns

### Chaining Multiple Hooks

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          "prettier --write $CLAUDE_FILE_PATH 2>/dev/null || true",
          "eslint --fix $CLAUDE_FILE_PATH 2>/dev/null || true",
          "echo '✓ Formatted and linted'"
        ]
      }
    ]
  }
}
```

### Different Hooks for Different File Types

```bash
#!/bin/bash
# scripts/auto-format.sh — format based on file extension
FILE="$1"
EXT="${FILE##*.}"

case "$EXT" in
    ts|tsx|js|jsx)
        prettier --write "$FILE" 2>/dev/null
        ;;
    py)
        ruff format "$FILE" 2>/dev/null
        ;;
    rs)
        rustfmt "$FILE" 2>/dev/null
        ;;
    go)
        gofmt -w "$FILE" 2>/dev/null
        ;;
esac
```

### Combining Project and Global Hooks

- **Global** (`~/.claude/settings.json`): Notifications, logging
- **Project** (`.claude/settings.json`): Linting, testing, validation

Both run — project hooks don't override global hooks.

---

## Non-Interactive Automation

Use Claude Code in scripts with the `-p` (print) flag:

### Automated Code Review

```bash
#!/bin/bash
# Review all changed files in a PR
git diff origin/main...HEAD --name-only | while read file; do
    echo "=== Reviewing: $file ==="
    cat "$file" | claude -p "Review this code for bugs, security issues, and style problems. Be concise."
    echo ""
done
```

### Batch Processing

```bash
#!/bin/bash
# Add type annotations to all Python files in a directory
find src/ -name "*.py" | while read file; do
    claude -p "Add type annotations to all functions in this file. Output only the modified file." < "$file" > "${file}.typed"
    mv "${file}.typed" "$file"
done
```

### Git Pre-Commit Hook

`.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Quick review of staged changes
DIFF=$(git diff --cached)
if [ -n "$DIFF" ]; then
    RESULT=$(echo "$DIFF" | claude -p "Review this diff. If there are critical issues (bugs, security vulnerabilities), list them. If everything looks fine, just say 'OK'." --max-turns 1)

    if [[ "$RESULT" != *"OK"* ]]; then
        echo "Claude Code review found issues:"
        echo "$RESULT"
        echo ""
        echo "Commit anyway? (y/n)"
        read -r answer
        if [ "$answer" != "y" ]; then
            exit 1
        fi
    fi
fi
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Claude Code Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Custom CI Script

```bash
#!/bin/bash
# ci/claude-review.sh — Run in CI pipeline
set -e

# Get the diff against the base branch
DIFF=$(git diff origin/main...HEAD)

# Review with Claude
REVIEW=$(echo "$DIFF" | claude -p \
  "Review this PR diff. Check for:
   1. Bugs and logic errors
   2. Security vulnerabilities
   3. Performance issues
   4. Missing error handling
   Output a markdown summary." \
  --output-format text \
  --max-turns 3)

# Post review as PR comment (using gh CLI)
echo "$REVIEW" | gh pr comment --body-file -
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook doesn't run | Check matcher matches the tool name exactly |
| Hook blocks everything | Ensure non-zero exit only for actual blocks |
| Hook output not visible | Hooks output goes to Claude as feedback |
| Hook slows Claude down | Keep hooks fast (<1 second), use async where possible |
| Permission denied | Make hook scripts executable: `chmod +x script.sh` |

### Debugging Hooks

Add logging to understand what's happening:

```bash
#!/bin/bash
# Debug hook — log all invocations
echo "$(date -Iseconds) | Tool: $CLAUDE_TOOL_NAME | File: $CLAUDE_FILE_PATH" >> /tmp/claude-hooks.log
```

---

<p align="center">
  <strong>Next:</strong> <a href="05-mcp-servers.md">MCP Servers</a> — Extend Claude's capabilities
</p>
