# Awesome Claude Resources

> A curated list of tools, libraries, MCP servers, articles, and resources for the Claude ecosystem.
>
> 精选的 Claude 生态工具、库、MCP 服务器、文章和资源列表。

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).
欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## Table of Contents / 目录

- [Official Resources / 官方资源](#official-resources)
- [Claude Code](#claude-code)
  - [Tips & Tricks / 技巧与窍门](#tips--tricks)
  - [MCP Servers / MCP 服务器](#mcp-servers)
  - [Hooks & Automation / 钩子与自动化](#hooks--automation)
  - [CLAUDE.md Examples / CLAUDE.md 示例](#claudemd-examples)
- [API & SDK](#api--sdk)
  - [Official SDKs / 官方 SDK](#official-sdks)
  - [Community Libraries / 社区库](#community-libraries)
- [Agent SDK / 智能体 SDK](#agent-sdk)
- [Prompt Engineering / 提示工程](#prompt-engineering)
- [Tools & Applications / 工具与应用](#tools--applications)
- [Tutorials & Articles / 教程与文章](#tutorials--articles)
- [Videos & Courses / 视频与课程](#videos--courses)
- [Community / 社区](#community)

---

## Official Resources / 官方资源

- [Claude](https://claude.ai) — Claude web interface / Claude 网页界面
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic's official CLI for Claude / Anthropic 官方 Claude 命令行工具
- [Anthropic API Docs](https://docs.anthropic.com) — Official API documentation / 官方 API 文档
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — Official code examples and guides / 官方代码示例和指南
- [Anthropic SDK (Python)](https://github.com/anthropics/anthropic-sdk-python) — Official Python SDK / 官方 Python SDK
- [Anthropic SDK (TypeScript)](https://github.com/anthropics/anthropic-sdk-typescript) — Official TypeScript SDK / 官方 TypeScript SDK
- [Model Context Protocol](https://modelcontextprotocol.io) — MCP specification and documentation / MCP 规范和文档
- [Claude Code Action](https://github.com/anthropics/claude-code-action) — GitHub Action for Claude Code / Claude Code 的 GitHub Action

---

## Claude Code

### Tips & Tricks / 技巧与窍门

- Use `CLAUDE.md` at project root — this is the single biggest productivity improvement — 在项目根目录使用 `CLAUDE.md`，这是最大的生产力提升
- Run `/init` on any new project to generate a starter `CLAUDE.md` — 在任何新项目上运行 `/init` 生成初始 `CLAUDE.md`
- Use `Shift+Tab` to toggle Plan mode for complex tasks — 使用 `Shift+Tab` 切换规划模式处理复杂任务
- Pipe files and diffs for quick analysis: `git diff | claude "review this"` — 通过管道传输文件和差异进行快速分析
- Use `/compact` before context runs out, not after — 在上下文用完之前使用 `/compact`，而不是之后
- Add frequently used commands to `.claude/settings.json` permissions — 将常用命令添加到 `.claude/settings.json` 权限中

### MCP Servers / MCP 服务器

#### Official / Anthropic-maintained / 官方维护
- [@anthropic-ai/mcp-filesystem](https://www.npmjs.com/package/@anthropic-ai/mcp-filesystem) — File system access with controlled permissions / 受控权限的文件系统访问
- [@anthropic-ai/mcp-github](https://www.npmjs.com/package/@anthropic-ai/mcp-github) — GitHub integration (issues, PRs, repos) / GitHub 集成（Issues、PR、仓库）

#### Popular Community MCP Servers / 热门社区 MCP 服务器
- [mcp-server-sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite) — SQLite database access / SQLite 数据库访问
- [mcp-server-postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) — PostgreSQL database access / PostgreSQL 数据库访问
- [mcp-server-puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer) — Browser automation / 浏览器自动化
- [mcp-server-brave-search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search) — Web search via Brave / 通过 Brave 进行网页搜索
- [mcp-server-memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) — Persistent memory for conversations / 对话持久化记忆
- [mcp-server-fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) — HTTP request capabilities / HTTP 请求功能
- [mcp-server-context7](https://github.com/upstash/context7) — Documentation context for any library / 任意库的文档上下文
- [mcp-server-playwright](https://github.com/anthropics/mcp-server-playwright) — Browser testing and automation / 浏览器测试与自动化

> See [MCP Servers Repository](https://github.com/modelcontextprotocol/servers) for the full official list.
> 查看 [MCP 服务器仓库](https://github.com/modelcontextprotocol/servers) 获取完整官方列表。

### Hooks & Automation / 钩子与自动化

Hooks let you run shell commands when Claude Code events occur:
（钩子允许你在 Claude Code 事件发生时运行 Shell 命令：）

| Event / 事件 | Use Case / 使用场景 |
|-------|----------|
| `PreToolUse` | Validate before file edits, check permissions / 编辑文件前验证，检查权限 |
| `PostToolUse` | Auto-lint after edits, run tests / 编辑后自动检查，运行测试 |
| `UserPromptSubmit` | Log prompts, add context / 记录提示词，添加上下文 |
| `Stop` | Notify when done, run final checks / 完成时通知，运行最终检查 |

### CLAUDE.md Examples / CLAUDE.md 示例

See our [templates directory](templates/) for ready-to-use CLAUDE.md files:
（查看我们的 [模板目录](templates/) 获取即用型 CLAUDE.md 文件：）
- [Universal template / 通用模板](templates/CLAUDE.md)
- [Python project / Python 项目](templates/CLAUDE-python.md)
- [TypeScript project / TypeScript 项目](templates/CLAUDE-typescript.md)
- [Rust project / Rust 项目](templates/CLAUDE-rust.md)

---

## API & SDK

### Official SDKs / 官方 SDK

| SDK | Language / 语言 | Links / 链接 |
|-----|----------|-------|
| anthropic-sdk-python | Python | [GitHub](https://github.com/anthropics/anthropic-sdk-python) · [PyPI](https://pypi.org/project/anthropic/) |
| anthropic-sdk-typescript | TypeScript | [GitHub](https://github.com/anthropics/anthropic-sdk-typescript) · [npm](https://www.npmjs.com/package/@anthropic-ai/sdk) |

### Community Libraries / 社区库

- [anthropic-go](https://github.com/anthropics/anthropic-sdk-go) — Go SDK
- [anthropic-rs](https://github.com/anthropics/anthropic-sdk-rust) — Rust SDK

---

## Agent SDK / 智能体 SDK

- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) — Build custom agents with tool use, memory, and orchestration / 构建具有工具使用、记忆和编排功能的自定义智能体

### Agent Patterns / 智能体模式

| Pattern / 模式 | Description / 描述 |
|---------|-------------|
| Simple Agent / 简单智能体 | Single agent with tools / 带工具的单个智能体 |
| Router Agent / 路由智能体 | Routes tasks to specialized sub-agents / 将任务路由到专门的子智能体 |
| Pipeline Agent / 管道智能体 | Sequential processing stages / 顺序处理阶段 |
| Parallel Agent / 并行智能体 | Concurrent execution with result aggregation / 并发执行并聚合结果 |

---

## Prompt Engineering / 提示工程

### Key Techniques for Claude / Claude 关键技巧

| Technique / 技巧 | Description / 描述 |
|-----------|-------------|
| XML Tags / XML 标签 | Use `<tag>` sections for structured input — Claude excels at this / 使用 `<tag>` 进行结构化输入，Claude 擅长处理此类格式 |
| System Prompts / 系统提示词 | Persistent instructions for role, format, constraints / 用于角色、格式、约束的持久指令 |
| Few-shot Examples / 少样本示例 | Provide input/output examples for consistent formatting / 提供输入/输出示例以保持格式一致 |
| Chain of Thought / 思维链 | "Think step by step" for complex reasoning / "逐步思考" 用于复杂推理 |
| Prefilling / 预填充 | Start assistant response to guide output format / 预填充助手回复以引导输出格式 |
| Extended Thinking / 扩展思考 | Enable for complex multi-step reasoning / 启用以进行复杂的多步推理 |

### Resources / 资源

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — Official guide / 官方指南
- [Prompt Library](https://docs.anthropic.com/en/prompt-library) — Official prompt examples / 官方提示词示例

---

## Tools & Applications / 工具与应用

### Development Tools / 开发工具
- [Claude Code](https://github.com/anthropics/claude-code) — CLI for software engineering / 软件工程命令行工具
- [Claude Code Action](https://github.com/anthropics/claude-code-action) — GitHub Actions integration / GitHub Actions 集成

### IDE Extensions / IDE 扩展
- Claude Code for VS Code
- Claude Code for JetBrains

### AI Coding Agents / AI 编码 Agent
- [Aider](https://github.com/paul-gauthier/aider) — Terminal AI coding with multi-model support and git integration / 终端 AI 编码，支持多模型和 git 集成
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) — Open-source AI software engineering agent (formerly OpenDevin) / 开源 AI 软件工程 Agent（原 OpenDevin）
- [SWE-agent](https://github.com/princeton-nlp/SWE-agent) — Princeton's autonomous bug-fixing agent for SWE-bench / Princeton 自动修 bug Agent

---

## Tutorials & Articles / 教程与文章

### Getting Started / 入门指南
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) — Official docs / 官方文档
- [Getting Started with Claude API](https://docs.anthropic.com/en/docs/quickstart) — API quickstart / API 快速入门

### Deep Dives / 深入探索
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Function calling / 函数调用
- [Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) — Complex reasoning / 复杂推理
- [Vision / Multimodal](https://docs.anthropic.com/en/docs/build-with-claude/vision) — Image understanding / 图像理解
- [Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming) — Real-time responses / 实时响应

---

## Videos & Courses / 视频与课程

*Coming soon — contributions welcome!*
*即将推出，欢迎贡献！*

---

## Community / 社区

- [r/ClaudeAI](https://reddit.com/r/ClaudeAI) — Reddit community / Reddit 社区
- [Anthropic Discord](https://discord.gg/anthropic) — Official Discord / 官方 Discord
- [Claude Code GitHub Issues](https://github.com/anthropics/claude-code/issues) — Bug reports and feature requests / Bug 报告和功能请求

---

<p align="center">
  <sub>Part of <a href="README.md">claude-engineer</a> — contributions welcome!</sub>
</p>
