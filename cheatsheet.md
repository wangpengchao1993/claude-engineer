# Claude Cheatsheet / Claude 速查表

> A quick reference for Claude Code CLI, API, and Prompt Engineering.
> Claude Code CLI、API 和 Prompt 工程速查表。

---

## Table of Contents / 目录

- [Claude Code CLI](#claude-code-cli)
- [Slash Commands](#slash-commands)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [CLI Flags](#cli-flags)
- [CLAUDE.md](#claudemd)
- [Hooks](#hooks)
- [MCP](#mcp)
- [API Quick Reference](#api-quick-reference)
- [Prompt Engineering Tips](#prompt-engineering-tips)

---

## Claude Code CLI

### Starting a Session / 启动会话

```bash
# Interactive mode / 交互模式
claude

# One-shot query / 一次性查询
claude "explain this error"

# Resume last conversation / 恢复上次对话
claude -c

# Resume specific conversation / 恢复指定对话
claude -c <conversation-id>

# Pipe input / 管道输入
cat error.log | claude "what went wrong?"
git diff | claude "review this change"

# Start with specific model / 指定模型
claude --model claude-sonnet-4-6

# Non-interactive (for scripts) / 非交互模式（用于脚本）
claude -p "generate a UUID"

# Output as JSON / JSON 输出
claude -p "list 5 colors" --output-format json

# Multi-turn with pipes / 管道多轮对话
echo "first question" | claude -p | claude -c -p "follow up"
```

### Key Concepts / 核心概念

| Concept | Description (EN) | 说明 (ZH) |
|---------|------------------|-----------|
| CLAUDE.md | Project config file loaded automatically | 项目配置文件，自动加载 |
| Hooks | Shell commands triggered by events | 事件触发的 Shell 命令 |
| MCP | Protocol to extend Claude's tools | 扩展 Claude 工具的协议 |
| Plan Mode | Think first, then act (Shift+Tab) | 先思考再行动 |
| Compact | Compress context when window fills | 上下文满时压缩 |
| Subagents | Parallel agents for complex tasks | 并行处理复杂任务的子 Agent |

---

## Slash Commands

| Command | Description | 说明 |
|---------|-------------|------|
| `/help` | Show help | 显示帮助 |
| `/init` | Generate CLAUDE.md for current project | 为当前项目生成 CLAUDE.md |
| `/compact` | Compress conversation context | 压缩对话上下文 |
| `/cost` | Show token usage and cost | 显示 Token 用量和费用 |
| `/mcp` | Manage MCP servers | 管理 MCP 服务器 |
| `/model` | Switch model | 切换模型 |
| `/memory` | Edit CLAUDE.md memory files | 编辑记忆文件 |
| `/review` | Code review changes | 代码审查 |
| `/pr-comments` | View PR comments | 查看 PR 评论 |
| `/clear` | Clear conversation history | 清除对话历史 |
| `/fast` | Toggle fast mode (same model, faster output) | 切换快速模式 |

---

## Keyboard Shortcuts

| Shortcut | Action | 操作 |
|----------|--------|------|
| `Enter` | Send message | 发送消息 |
| `Shift+Enter` | New line | 换行 |
| `Shift+Tab` | Toggle Plan mode | 切换 Plan 模式 |
| `Esc` (1x) | Cancel current input | 取消当前输入 |
| `Esc` (2x) | Interrupt Claude | 中断 Claude 生成 |
| `Ctrl+C` | Exit / Abort | 退出/中止 |
| `Up Arrow` | Cycle through previous messages | 浏览历史消息 |
| `!command` | Run shell command inline | 内联运行 Shell 命令 |

---

## CLI Flags

```bash
claude [options] [prompt]

Options:
  -c, --continue           # Resume last conversation / 恢复上次对话
  -p, --print              # Non-interactive, print response / 非交互，打印响应
  --model <model>          # Specify model / 指定模型
  --output-format <fmt>    # Output format: text, json, stream-json
  --max-turns <n>          # Max agentic turns / 最大 Agent 轮次
  --system-prompt <text>   # Override system prompt (with -p only)
  --allowedTools <tools>   # Restrict available tools / 限制可用工具
  --disallowedTools <t>    # Exclude specific tools / 排除特定工具
  --permission-mode <mode> # default, plan, bypassPermissions
  --add-dir <path>         # Add extra directory context / 添加额外目录上下文
  --verbose                # Show detailed logs / 显示详细日志
```

---

## CLAUDE.md

### File Locations / 文件位置

| Location | Scope | Shared? | 范围 |
|----------|-------|---------|------|
| `./CLAUDE.md` | Project root | Yes (commit to git) | 项目级（提交到 git） |
| `./some/dir/CLAUDE.md` | Directory-specific | Yes | 目录级 |
| `~/.claude/CLAUDE.md` | User-global | No | 用户全局 |

### Effective Template / 实用模板

```markdown
# Project: My App

## Overview
Brief description of the project purpose and architecture.

## Tech Stack
- Language: Python 3.12
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy 2.0
- Testing: pytest

## Commands
- `make dev` — Start development server
- `make test` — Run all tests
- `make lint` — Run ruff linter
- `make fmt` — Auto-format code

## Architecture
- `src/api/` — API route handlers
- `src/models/` — Database models
- `src/services/` — Business logic
- `src/utils/` — Shared utilities
- `tests/` — Test files mirror src/ structure

## Code Conventions
- Type hints on all function signatures
- Docstrings for public functions (Google style)
- Async by default for I/O operations
- Use dependency injection for services
- Tests follow arrange-act-assert pattern

## Important Notes
- Never modify migration files manually
- All API responses use the ResponseModel wrapper
- Environment variables are loaded via src/config.py
```

---

## Hooks

Hooks are shell commands triggered by Claude Code events. Configure in `.claude/settings.json`:

```jsonc
{
  "hooks": {
    // Before any edit to a file
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["./scripts/check-file-lock.sh $CLAUDE_FILE_PATH"]
      }
    ],
    // After any edit to a file
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["npm run lint --fix $CLAUDE_FILE_PATH"]
      }
    ],
    // When user submits a prompt
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": ["./scripts/log-prompt.sh"]
      }
    ],
    // When Claude stops responding
    "Stop": [
      {
        "matcher": "",
        "hooks": ["./scripts/notify-done.sh"]
      }
    ]
  }
}
```

### Hook Events / Hook 事件

| Event | When | 触发时机 |
|-------|------|----------|
| `PreToolUse` | Before a tool is called | 工具调用前 |
| `PostToolUse` | After a tool is called | 工具调用后 |
| `UserPromptSubmit` | When user submits a message | 用户提交消息时 |
| `Stop` | When Claude finishes responding | Claude 完成响应时 |

---

## MCP

### Adding an MCP Server / 添加 MCP 服务器

```bash
# Add via CLI
claude mcp add <name> <command> [args...]

# Example: Add a filesystem MCP server
claude mcp add filesystem npx @anthropic-ai/mcp-filesystem /path/to/dir

# Example: Add GitHub MCP server
claude mcp add github npx @anthropic-ai/mcp-github

# List MCP servers
claude mcp list

# Remove an MCP server
claude mcp remove <name>
```

### MCP Config in settings.json

```jsonc
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

---

## API Quick Reference

### Python SDK

```python
import anthropic

client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

# Basic message
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(response.content[0].text)
```

### TypeScript SDK

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // Uses ANTHROPIC_API_KEY env var

const response = await client.messages.create({
  model: "claude-sonnet-4-6-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude!" }],
});
console.log(response.content[0].text);
```

### Tool Use (Function Calling)

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Key API Parameters / API 关键参数

| Parameter | Type | Description | 说明 |
|-----------|------|-------------|------|
| `model` | string | Model ID | 模型 ID |
| `max_tokens` | int | Max output tokens | 最大输出 Token 数 |
| `messages` | array | Conversation messages | 对话消息列表 |
| `system` | string | System prompt | 系统 Prompt |
| `temperature` | float | Randomness (0-1) | 随机性（0-1） |
| `top_p` | float | Nucleus sampling | 核采样 |
| `tools` | array | Available tools | 可用工具 |
| `tool_choice` | object | Tool selection strategy | 工具选择策略 |
| `stream` | bool | Enable streaming | 启用流式输出 |

### Models / 模型

| Model | ID | Best For | 适用场景 |
|-------|-------|----------|----------|
| Opus 4.6 | `claude-opus-4-6` | Complex tasks, coding | 复杂任务、编程 |
| Sonnet 4.6 | `claude-sonnet-4-6` | Balanced performance | 性能平衡 |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast, lightweight | 快速、轻量 |

---

## Prompt Engineering Tips

### Structure Your Prompts / 结构化你的 Prompt

```
Role: You are a [specific role].

Context: [Background information]

Task: [Clear, specific instruction]

Format: [Expected output format]

Constraints:
- [Constraint 1]
- [Constraint 2]
```

### Best Practices / 最佳实践

| Tip | Example | 示例 |
|-----|---------|------|
| Be specific | "Refactor to use async/await" not "improve code" | "重构为 async/await" 而非 "改善代码" |
| Provide context | "In this Express.js app..." | "在这个 Express.js 应用中..." |
| Show examples | "Format like: `{name}: {value}`" | "格式如：`{名称}: {值}`" |
| Set constraints | "Under 50 lines, no external deps" | "不超过50行，不用外部依赖" |
| Chain tasks | Break complex work into steps | 将复杂工作拆分为步骤 |

### Claude-Specific Tips / Claude 专属技巧

1. **Use XML tags for structure** — Claude excels at understanding XML-tagged sections:
   ```
   <context>The app uses React 18</context>
   <task>Add error boundary to UserProfile component</task>
   <constraints>No class components, use react-error-boundary library</constraints>
   ```

2. **Think step by step** — Add "Think step by step" for complex reasoning tasks.

3. **Prefill assistant response** — Guide output format by starting the assistant message:
   ```python
   messages=[
       {"role": "user", "content": "List 3 colors in JSON"},
       {"role": "assistant", "content": "["}  # Forces JSON array output
   ]
   ```

4. **Use system prompt for persistent instructions** — Put role, rules, and formatting in the system prompt.

5. **Extended thinking** — For complex tasks, enable extended thinking to let Claude reason before answering.

---

## Environment Variables / 环境变量

| Variable | Description | 说明 |
|----------|-------------|------|
| `ANTHROPIC_API_KEY` | API key for Claude | Claude API 密钥 |
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock | 使用 AWS Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI | 使用 Google Vertex AI |
| `ANTHROPIC_MODEL` | Default model override | 默认模型覆盖 |

---

<p align="center">
  <sub>Part of <a href="README.md">claude-engineer</a> — give it a star if this helped!</sub>
</p>
