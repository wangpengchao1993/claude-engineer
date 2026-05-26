# Claude 速查表

> Claude Code CLI、API 和 Prompt 工程中文速查表。
>
> English version: [cheatsheet.md](cheatsheet.md)

---

## 目录

- [Claude Code CLI](#claude-code-cli)
- [斜杠命令](#斜杠命令)
- [快捷键](#快捷键)
- [命令行参数](#命令行参数)
- [CLAUDE.md](#claudemd)
- [Hooks 钩子](#hooks-钩子)
- [MCP 协议](#mcp-协议)
- [API 速查](#api-速查)
- [Prompt 工程技巧](#prompt-工程技巧)

---

## Claude Code CLI

### 运行平台

Claude Code 可在多个平台运行：

| 平台 | 说明 |
|------|------|
| **终端 CLI** | 主力形态，`claude` 命令启动 |
| **桌面应用** | macOS / Windows 原生应用 |
| **Web 应用** | 浏览器中使用（claude.ai/code） |
| **VS Code 扩展** | 在 VS Code 中使用 Claude Code |
| **JetBrains 插件** | IntelliJ / PyCharm / WebStorm 等 |

### 启动会话

```bash
# 交互模式
claude

# 一次性查询
claude "解释这个错误"

# 恢复上次对话
claude -c

# 恢复指定对话
claude -c <conversation-id>

# 管道输入
cat error.log | claude "哪里出了问题？"
git diff | claude "review this change"

# 指定模型
claude --model claude-sonnet-4-6

# 非交互模式（用于脚本/CI）
claude -p "生成一个 UUID"

# JSON 输出
claude -p "列出5种颜色" --output-format json

# 管道多轮对话
echo "第一个问题" | claude -p | claude -c -p "追问"
```

### 核心概念

| 概念 | 说明 |
|------|------|
| CLAUDE.md | 项目配置文件，启动时自动加载，是"上下文工程"的核心载体 |
| Hooks | 事件触发的 Shell 命令（编辑前检查、编辑后 lint 等） |
| MCP | Model Context Protocol，扩展 Claude 工具能力的协议 |
| Plan 模式 | 先规划再执行（Shift+Tab 切换） |
| /compact | 上下文快满时压缩对话，提前用而不是等到溢出 |
| 子 Agent | Claude 自动启动的并行 Agent，处理复杂任务 |
| Memory | 跨对话持久化记忆系统（auto-memory） |
| Skills | 自定义斜杠命令（`.claude/commands/` 或 `.claude/skills/`） |

---

## 斜杠命令

### 常用命令

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助 |
| `/init` | 为当前项目生成 CLAUDE.md |
| `/compact` | 压缩对话上下文 |
| `/cost` | 显示 Token 用量和费用 |
| `/clear` | 清除对话历史 |
| `/model` | 切换模型 |
| `/fast` | 切换快速模式（同模型，更快输出） |

### 工作流命令

| 命令 | 说明 |
|------|------|
| `/plan` | 进入 Plan 模式 |
| `/review` | 代码审查当前改动 |
| `/memory` | 编辑记忆文件 |
| `/mcp` | 管理 MCP 服务器 |
| `/permissions` | 管理权限设置 |
| `/diff` | 查看当前改动的 diff |
| `/context` | 查看上下文使用情况 |

> 使用 `/help` 查看完整命令列表。Claude Code 持续更新中，新命令可能随版本增加。

---

## 快捷键

| 快捷键 | 操作 |
|--------|------|
| `Enter` | 发送消息 |
| `Ctrl+J` | 换行（多行输入） |
| `Shift+Tab` | 切换 Plan 模式 |
| `Esc` | 取消当前输入 / 中断 Claude 生成 |
| `Ctrl+C` | 中断 / 退出 |
| `Ctrl+D` | 退出 Claude Code |
| `↑ 方向键` | 浏览历史消息 |
| `Ctrl+L` | 清除输入 |
| `Ctrl+R` | 搜索历史 |

> 快捷键可通过 `~/.claude/keybindings.json` 自定义。

---

## 命令行参数

```bash
claude [选项] [prompt]

常用选项:
  -c, --continue           # 恢复上次对话
  -p, --print              # 非交互模式，直接打印响应（适合脚本/CI）
  --model <model>          # 指定模型
  --output-format <fmt>    # 输出格式: text, json, stream-json
  --max-turns <n>          # 最大 Agent 轮次
  --system-prompt <text>   # 覆盖系统 prompt（仅 -p 模式）
  --allowedTools <tools>   # 限制可用工具
  --disallowedTools <t>    # 排除特定工具
  --permission-mode <mode> # default, plan, bypassPermissions
  --add-dir <path>         # 添加额外目录上下文
  --verbose                # 显示详细日志
  --resume <id>            # 按 ID 恢复指定对话
  --mcp-config <path>      # 加载 MCP 配置文件
```

---

## CLAUDE.md

### 文件位置与加载顺序

CLAUDE.md 支持多层级，**叠加加载**（不是覆盖）：

| 位置 | 范围 | 是否提交到 git |
|------|------|---------------|
| `./CLAUDE.md` | 项目根目录级 | 是（团队共享） |
| `./some/dir/CLAUDE.md` | 子目录级（进入该目录时加载） | 是 |
| `./.claude/CLAUDE.md` | 项目私有配置 | 否（加入 .gitignore） |
| `./.claude/rules/*.md` | 按路径匹配的细粒度规则 | 可选 |
| `~/.claude/CLAUDE.md` | 用户全局（所有项目生效） | 否 |

### 实用模板

```markdown
# 项目名称

## 概述
简要说明项目用途和架构。

## 技术栈
- 语言: Python 3.12
- 框架: FastAPI
- 数据库: PostgreSQL
- ORM: SQLAlchemy 2.0
- 测试: pytest

## 常用命令
- `make dev` — 启动开发服务器
- `make test` — 运行所有测试
- `make lint` — 运行 linter
- `make fmt` — 自动格式化

## 项目结构
- `src/api/` — API 路由处理
- `src/models/` — 数据库模型
- `src/services/` — 业务逻辑
- `src/utils/` — 公共工具
- `tests/` — 测试文件（与 src/ 镜像）

## 代码规范
- 所有函数签名必须有类型注解
- 公共函数需写 docstring（Google 风格）
- I/O 操作默认使用 async
- 测试遵循 Arrange-Act-Assert 模式

## 注意事项
- 不要手动修改 migration 文件
- 所有 API 响应使用 ResponseModel 包装
- 环境变量通过 src/config.py 加载
```

---

## Hooks 钩子

Hooks 是 Claude Code 事件触发的 Shell 命令，在 `.claude/settings.json` 中配置。

### 核心 Hook 事件

| 事件 | 触发时机 | 典型用途 |
|------|----------|---------|
| `PreToolUse` | 工具调用前（可拦截） | 编辑前检查文件锁、保护文件 |
| `PostToolUse` | 工具调用后 | 自动 lint/格式化 |
| `UserPromptSubmit` | 用户提交消息时 | 日志记录、prompt 过滤 |
| `Stop` | Claude 完成响应时 | 桌面通知、汇总统计 |

### 更多 Hook 事件

Claude Code 还支持更多事件类型，包括：

| 事件 | 触发时机 |
|------|----------|
| `SessionStart` / `SessionEnd` | 会话开始/结束 |
| `SubagentStart` / `SubagentStop` | 子 Agent 启动/停止 |
| `PreCompact` / `PostCompact` | 上下文压缩前后 |
| `FileChanged` | 文件变更时 |
| `TaskCreated` / `TaskCompleted` | 任务创建/完成 |

> 完整事件列表见 [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)。

### 配置示例

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["./scripts/check-file-lock.sh $CLAUDE_FILE_PATH"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": ["npm run lint --fix $CLAUDE_FILE_PATH"]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": ["./scripts/notify-done.sh"]
      }
    ]
  }
}
```

---

## MCP 协议

### 添加 MCP 服务器

```bash
# 通过 CLI 添加
claude mcp add <名称> <命令> [参数...]

# 添加文件系统 MCP
claude mcp add filesystem npx @anthropic-ai/mcp-filesystem /path/to/dir

# 添加 GitHub MCP
claude mcp add github npx @anthropic-ai/mcp-github

# 列出已添加的 MCP
claude mcp list

# 移除 MCP
claude mcp remove <名称>
```

### 在 settings.json 中配置

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

## API 速查

### Python SDK

```python
import anthropic

client = anthropic.Anthropic()  # 使用 ANTHROPIC_API_KEY 环境变量

# 基础消息
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好，Claude！"}]
)
print(response.content[0].text)
```

### TypeScript SDK

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // 使用 ANTHROPIC_API_KEY 环境变量

const response = await client.messages.create({
  model: "claude-sonnet-4-6-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "你好，Claude！" }],
});
console.log(response.content[0].text);
```

### Tool Use（函数调用）

```python
response = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "获取指定城市的当前天气",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名称"}
            },
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "东京现在天气怎么样？"}]
)
```

### 流式输出

```python
with client.messages.stream(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "写一个故事"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### API 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型 ID |
| `max_tokens` | int | 最大输出 Token 数 |
| `messages` | array | 对话消息列表 |
| `system` | string | 系统 Prompt |
| `temperature` | float | 随机性（0-1，默认 1） |
| `tools` | array | 可用工具定义 |
| `tool_choice` | object | 工具选择策略 |
| `stream` | bool | 启用流式输出 |

### 模型选择

| 模型 | ID | 适用场景 |
|------|-----|----------|
| Opus 4.6 | `claude-opus-4-6` | 复杂推理、编程、架构设计 |
| Sonnet 4.6 | `claude-sonnet-4-6` | 日常开发、性价比最优 |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | 快速响应、轻量任务、批处理 |

> 上下文窗口：默认 200K tokens。通过 Amazon Bedrock 或 Google Vertex AI 可使用 1M tokens 上下文。

---

## Prompt 工程技巧

### 结构化你的 Prompt

```
角色: 你是一个 [具体角色]。

上下文: [背景信息]

任务: [清晰、具体的指令]

输出格式: [期望的输出格式]

约束:
- [约束 1]
- [约束 2]
```

### 最佳实践

| 技巧 | 反面 | 正面 |
|------|------|------|
| 具体明确 | "改善代码" | "重构为 async/await，去掉回调嵌套" |
| 提供上下文 | "修复认证 bug" | "JWT 过期后 refresh token 仍有效但返回 401…" |
| 给出示例 | "格式化输出" | "格式如：`{名称}: {值}`" |
| 设定约束 | "写个脚本" | "不超过 50 行，不用外部依赖，兼容 Python 3.9+" |
| 拆分步骤 | 一口气描述所有需求 | 分步骤让 Claude 逐个完成 |

### Claude 专属技巧

1. **用 XML 标签组织信息** — Claude 对 XML 标签的理解特别好：
   ```
   <context>项目使用 React 18</context>
   <task>为 UserProfile 组件添加错误边界</task>
   <constraints>不用 class 组件，使用 react-error-boundary 库</constraints>
   ```

2. **"逐步思考"** — 复杂推理任务加上 "Think step by step"。

3. **预填充助手回复** — 通过开头引导输出格式：
   ```python
   messages=[
       {"role": "user", "content": "列出3种颜色，用 JSON"},
       {"role": "assistant", "content": "["}  # 强制 JSON 数组输出
   ]
   ```

4. **System Prompt 放持久指令** — 角色、规则、格式要求放到 system prompt 中。

5. **Extended Thinking** — 复杂任务启用扩展思考，让 Claude 先推理再回答。

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Claude API 密钥 |
| `ANTHROPIC_MODEL` | 覆盖默认模型 |
| `CLAUDE_CODE_USE_BEDROCK` | 启用 AWS Bedrock 后端 |
| `CLAUDE_CODE_USE_VERTEX` | 启用 Google Vertex AI 后端 |

> Bedrock/Vertex 需要额外配置对应云平台的认证信息（AWS credentials / GCP service account）。
> 完整环境变量列表见官方文档。

---

<p align="center">
  <sub>来自 <a href="README.md">claude-engineer</a> — 觉得有用请给个 Star！</sub>
</p>
