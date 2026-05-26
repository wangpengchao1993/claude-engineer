# Hooks 与自动化

> 用 Hooks 自动化你的 Claude Code 工作流 — 事件触发 Shell 命令、强制执行标准、构建自定义流水线。

## 目录

- [什么是 Hooks？](#什么是-hooks)
- [Hook 事件](#hook-事件)
- [配置方法](#配置方法)
- [实用示例](#实用示例)
- [Hook 环境变量](#hook-环境变量)
- [高级模式](#高级模式)
- [非交互自动化](#非交互自动化)
- [CI/CD 集成](#cicd-集成)

---

## 什么是 Hooks？

Hooks 是在 Claude Code 特定事件发生时自动运行的 Shell 命令。可以用来：

- **自动 lint** — Claude 编辑文件后自动格式化
- **运行测试** — 代码变更后自动测试
- **记录提示** — 审计用途
- **发送通知** — Claude 完成时提醒
- **验证变更** — 应用前检查
- **强制规则** — 项目特定规则

配置在 `.claude/settings.json`（项目级）或 `~/.claude/settings.json`（全局）。

---

## Hook 事件

| 事件 | 触发时机 | 常见用途 |
|------|----------|----------|
| `PreToolUse` | Claude 调用工具之前 | 验证、阻止、修改工具调用 |
| `PostToolUse` | 工具调用完成之后 | 自动 lint、自动测试、记录变更 |
| `UserPromptSubmit` | 用户发送消息时 | 添加上下文、记录提示 |
| `Stop` | Claude 完成响应时 | 通知、最终检查 |

### 事件流程

```
用户发送消息
    │
    ├─► [UserPromptSubmit hooks 运行]
    │
    ▼
Claude 处理并决定使用工具
    │
    ├─► [PreToolUse hooks 运行]
    │       │
    │       ├─ Hook 阻止 → 跳过工具
    │       └─ Hook 通过 → 工具执行
    │
    ├─► 工具执行 (Edit, Bash 等)
    │
    ├─► [PostToolUse hooks 运行]
    │
    ▼
Claude 完成响应
    │
    └─► [Stop hooks 运行]
```

---

## 配置方法

在 `.claude/settings.json` 中：

```jsonc
{
  "hooks": {
    "事件名": [
      {
        "matcher": "工具名",     // 匹配哪些工具
        "hooks": ["要运行的命令"]  // Shell 命令
      }
    ]
  }
}
```

### 匹配器模式

- `""` — 匹配所有工具/事件
- `"Edit"` — 只匹配 Edit 工具
- `"Edit|Write"` — 匹配 Edit 或 Write
- `"Bash"` — 匹配任何 Bash 命令

---

## 实用示例

### 1. 编辑后自动 Lint

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

**Python 版本：**

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

### 2. 防止编辑受保护文件

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["./scripts/check-protected.sh $CLAUDE_FILE_PATH"]
      }
    ]
  }
}
```

`scripts/check-protected.sh`：
```bash
#!/bin/bash
PROTECTED=("migrations/versions/" "generated/" ".env.production" "package-lock.json")
for pattern in "${PROTECTED[@]}"; do
    if [[ "$1" == *"$pattern"* ]]; then
        echo "阻止：$1 是受保护文件，不应被修改。"
        exit 1
    fi
done
```

### 3. 完成后桌面通知

```jsonc
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          "notify-send 'Claude Code' '任务完成！' 2>/dev/null || osascript -e 'display notification \"任务完成！\" with title \"Claude Code\"' 2>/dev/null || true"
        ]
      }
    ]
  }
}
```

### 4. 代码变更后运行测试

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["./scripts/run-related-tests.sh $CLAUDE_FILE_PATH"]
      }
    ]
  }
}
```

---

## Hook 环境变量

| 变量 | 可用于 | 描述 |
|------|--------|------|
| `$CLAUDE_FILE_PATH` | PreToolUse, PostToolUse | 被编辑的文件路径 |
| `$CLAUDE_TOOL_NAME` | PreToolUse, PostToolUse | 被调用的工具名 |
| `$CLAUDE_PROMPT` | UserPromptSubmit | 用户的提示文本 |

### 阻止工具调用

如果 `PreToolUse` hook 以**非零退出码**退出，工具调用会被阻止，Claude 会看到 hook 的输出作为反馈。

---

## 高级模式

### 按文件类型选择不同的 Hook

```bash
#!/bin/bash
# scripts/auto-format.sh
FILE="$1"
EXT="${FILE##*.}"

case "$EXT" in
    ts|tsx|js|jsx) prettier --write "$FILE" 2>/dev/null ;;
    py) ruff format "$FILE" 2>/dev/null ;;
    rs) rustfmt "$FILE" 2>/dev/null ;;
    go) gofmt -w "$FILE" 2>/dev/null ;;
esac
```

---

## 非交互自动化

用 `-p` 标志在脚本中使用 Claude Code：

### 自动代码审查

```bash
#!/bin/bash
git diff origin/main...HEAD --name-only | while read file; do
    echo "=== 审查：$file ==="
    cat "$file" | claude -p "审查这段代码，找出 bug、安全问题和风格问题。简洁明了。"
done
```

### Git Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
DIFF=$(git diff --cached)
if [ -n "$DIFF" ]; then
    RESULT=$(echo "$DIFF" | claude -p "审查这个 diff。如果有严重问题（bug、安全漏洞），列出来。没问题就说 'OK'。" --max-turns 1)
    if [[ "$RESULT" != *"OK"* ]]; then
        echo "Claude 审查发现问题："
        echo "$RESULT"
        exit 1
    fi
fi
```

---

## CI/CD 集成

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
      - name: Claude 审查
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

<p align="center">
  <strong>下一篇：</strong> <a href="05-mcp-servers.md">MCP 服务器</a> — 扩展 Claude 的能力
</p>

---

[← 上一章：CLAUDE.md 指南](03-claude-md-guide.md) | [目录](../../README_zh.md) | [下一章：MCP 服务器 →](05-mcp-servers.md)
