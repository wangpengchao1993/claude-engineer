# Awesome Claude Resources

> A curated list of tools, libraries, MCP servers, articles, and resources for the Claude ecosystem.
>
> 精选的 Claude 生态工具、库、MCP 服务器、文章和资源列表。

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Table of Contents

- [Official Resources](#official-resources)
- [Claude Code](#claude-code)
  - [Tips & Tricks](#tips--tricks)
  - [MCP Servers](#mcp-servers)
  - [Hooks & Automation](#hooks--automation)
  - [CLAUDE.md Examples](#claudemd-examples)
- [API & SDK](#api--sdk)
  - [Official SDKs](#official-sdks)
  - [Community Libraries](#community-libraries)
- [Agent SDK](#agent-sdk)
- [Prompt Engineering](#prompt-engineering)
- [Tools & Applications](#tools--applications)
- [Tutorials & Articles](#tutorials--articles)
- [Videos & Courses](#videos--courses)
- [Community](#community)

---

## Official Resources

- [Claude](https://claude.ai) — Claude web interface
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic's official CLI for Claude
- [Anthropic API Docs](https://docs.anthropic.com) — Official API documentation
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — Official code examples and guides
- [Anthropic SDK (Python)](https://github.com/anthropics/anthropic-sdk-python) — Official Python SDK
- [Anthropic SDK (TypeScript)](https://github.com/anthropics/anthropic-sdk-typescript) — Official TypeScript SDK
- [Model Context Protocol](https://modelcontextprotocol.io) — MCP specification and documentation
- [Claude Code Action](https://github.com/anthropics/claude-code-action) — GitHub Action for Claude Code

---

## Claude Code

### Tips & Tricks

- Use `CLAUDE.md` at project root — this is the single biggest productivity improvement
- Run `/init` on any new project to generate a starter `CLAUDE.md`
- Use `Shift+Tab` to toggle Plan mode for complex tasks
- Pipe files and diffs for quick analysis: `git diff | claude "review this"`
- Use `/compact` before context runs out, not after
- Add frequently used commands to `.claude/settings.json` permissions

### MCP Servers

#### Official / Anthropic-maintained
- [@anthropic-ai/mcp-filesystem](https://www.npmjs.com/package/@anthropic-ai/mcp-filesystem) — File system access with controlled permissions
- [@anthropic-ai/mcp-github](https://www.npmjs.com/package/@anthropic-ai/mcp-github) — GitHub integration (issues, PRs, repos)

#### Popular Community MCP Servers
- [mcp-server-sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite) — SQLite database access
- [mcp-server-postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) — PostgreSQL database access
- [mcp-server-puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer) — Browser automation
- [mcp-server-brave-search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search) — Web search via Brave
- [mcp-server-memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) — Persistent memory for conversations
- [mcp-server-fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) — HTTP request capabilities

> See [MCP Servers Repository](https://github.com/modelcontextprotocol/servers) for the full official list.

### Hooks & Automation

Hooks let you run shell commands when Claude Code events occur:

| Event | Use Case |
|-------|----------|
| `PreToolUse` | Validate before file edits, check permissions |
| `PostToolUse` | Auto-lint after edits, run tests |
| `UserPromptSubmit` | Log prompts, add context |
| `Stop` | Notify when done, run final checks |

### CLAUDE.md Examples

See our [templates directory](templates/) for ready-to-use CLAUDE.md files:
- [Universal template](templates/CLAUDE.md)
- [Python project](templates/CLAUDE-python.md)
- [TypeScript project](templates/CLAUDE-typescript.md)
- [Rust project](templates/CLAUDE-rust.md)

---

## API & SDK

### Official SDKs

| SDK | Language | Links |
|-----|----------|-------|
| anthropic-sdk-python | Python | [GitHub](https://github.com/anthropics/anthropic-sdk-python) · [PyPI](https://pypi.org/project/anthropic/) |
| anthropic-sdk-typescript | TypeScript | [GitHub](https://github.com/anthropics/anthropic-sdk-typescript) · [npm](https://www.npmjs.com/package/@anthropic-ai/sdk) |

### Community Libraries

- [anthropic-go](https://github.com/anthropics/anthropic-sdk-go) — Go SDK
- [anthropic-rs](https://github.com/anthropics/anthropic-sdk-rust) — Rust SDK

---

## Agent SDK

- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) — Build custom agents with tool use, memory, and orchestration

### Agent Patterns

| Pattern | Description |
|---------|-------------|
| Simple Agent | Single agent with tools |
| Router Agent | Routes tasks to specialized sub-agents |
| Pipeline Agent | Sequential processing stages |
| Parallel Agent | Concurrent execution with result aggregation |

---

## Prompt Engineering

### Key Techniques for Claude

| Technique | Description |
|-----------|-------------|
| XML Tags | Use `<tag>` sections for structured input — Claude excels at this |
| System Prompts | Persistent instructions for role, format, constraints |
| Few-shot Examples | Provide input/output examples for consistent formatting |
| Chain of Thought | "Think step by step" for complex reasoning |
| Prefilling | Start assistant response to guide output format |
| Extended Thinking | Enable for complex multi-step reasoning |

### Resources

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — Official guide
- [Prompt Library](https://docs.anthropic.com/en/prompt-library) — Official prompt examples

---

## Tools & Applications

### Development Tools
- [Claude Code](https://github.com/anthropics/claude-code) — CLI for software engineering
- [Claude Code Action](https://github.com/anthropics/claude-code-action) — GitHub Actions integration

### IDE Extensions
- Claude Code for VS Code
- Claude Code for JetBrains

---

## Tutorials & Articles

### Getting Started
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) — Official docs
- [Getting Started with Claude API](https://docs.anthropic.com/en/docs/quickstart) — API quickstart

### Deep Dives
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Function calling
- [Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) — Complex reasoning
- [Vision / Multimodal](https://docs.anthropic.com/en/docs/build-with-claude/vision) — Image understanding
- [Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming) — Real-time responses

---

## Videos & Courses

*Coming soon — contributions welcome!*

---

## Community

- [r/ClaudeAI](https://reddit.com/r/ClaudeAI) — Reddit community
- [Anthropic Discord](https://discord.gg/anthropic) — Official Discord
- [Claude Code GitHub Issues](https://github.com/anthropics/claude-code/issues) — Bug reports and feature requests

---

<p align="center">
  <sub>Part of <a href="README.md">claude-engineer</a> — contributions welcome!</sub>
</p>
