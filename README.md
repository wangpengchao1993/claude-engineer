<h1 align="center">Claude Engineer</h1>

<p align="center">
  <strong>The ultimate guide to mastering Claude — from Claude Code CLI to API to Agent SDK.</strong>
</p>

<p align="center">
  <a href="https://github.com/anthropics/claude-code"><img src="https://img.shields.io/badge/Claude%20Code-Latest-blueviolet?logo=anthropic" alt="Claude Code"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="README_zh.md"><img src="https://img.shields.io/badge/中文文档-点击查看-orange" alt="中文文档"></a>
</p>

---

## Why This Repo?

- **All-in-one reference** — Covers Claude Code CLI, API, Agent SDK, MCP, Prompt Engineering, and more in a single place.
- **Copy-paste ready** — Templates for `CLAUDE.md`, hooks, system prompts, and MCP configs you can use immediately.
- **Real-world examples** — Runnable code samples for agents, tool use, streaming, and automation workflows.

### Quick Start Map / 快速导航

| I want to... / 我想... | Go here / 去这里 |
|------------------------|-----------------|
| Get started from zero / 从零开始 | [guide/en/01](guide/en/01-getting-started.md) · [中文](guide/zh/01-getting-started.md) |
| Build a complete project with AI / 用 AI 做一个完整项目 | [guide/en/11](guide/en/11-end-to-end-project.md) · [中文](guide/zh/11-end-to-end-project.md) |
| Pick a workflow framework / 选一个工作流框架 | [frameworks/](examples/frameworks/) |
| Copy a CLAUDE.md template / 抄一个模板 | [templates/](templates/) — Python · C++ · Java · TS · Rust · Fullstack |
| Set up CI/CD with AI / 搭 AI 流水线 | [cicd-templates/](examples/cicd-templates/) |
| Save money on tokens / 省 Token 钱 | [guide/en/13](guide/en/13-cost-and-model-selection.md) · [中文](guide/zh/13-cost-and-model-selection.md) |

---

## Learning Roadmap

> Follow the path from beginner to expert. Full roadmap: [roadmap.md](roadmap.md)

```
🟢 Stage 1: Getting Started     🔵 Stage 2: Daily Driver
   Install → First Chat →          Interactive → Plan Mode →
   CLAUDE.md                       Git & Pipes → /compact

🟡 Stage 3: Power User          🔴 Stage 4: Expert
   Hooks → MCP Servers →           Claude API → Agent SDK →
   Prompt Engineering               Multi-Agent → CI/CD
```

---

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Roadmap](roadmap.md) | Step-by-step learning path from beginner to expert |
| [Cheatsheet](cheatsheet.md) | Quick reference for commands, shortcuts, and tips |
| [Guide](guide/en/) | In-depth tutorials from beginner to advanced |
| [Templates](templates/) | Ready-to-use CLAUDE.md, hooks, and prompt templates |
| [Examples](examples/) | Runnable code samples |
| [Awesome Resources](awesome.md) | Curated tools, MCP servers, articles, and more |

---

## Cheatsheet Highlights

> Full cheatsheet: [cheatsheet.md](cheatsheet.md)

### Claude Code Essential Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive REPL |
| `claude "query"` | One-shot query, no interactive session |
| `cat file \| claude "explain"` | Pipe content for analysis |
| `claude -c` | Resume most recent conversation |
| `claude --model` | Specify which model to use |
| `/init` | Generate a CLAUDE.md file for your project |
| `/compact` | Compress conversation context |
| `/mcp` | Manage MCP servers |
| `/cost` | Show token usage and cost |
| Shift+Tab | Toggle Plan mode (think before acting) |
| Esc (2x) | Interrupt Claude while generating |

### CLAUDE.md Quick Tips

```markdown
# CLAUDE.md — Put this at your project root

## Project Overview
Brief description of what this project does.

## Tech Stack
- Language: TypeScript
- Framework: Next.js 14
- Database: PostgreSQL with Prisma

## Commands
- `npm run dev` — Start development server
- `npm test` — Run tests
- `npm run lint` — Run linter

## Code Conventions
- Use functional components with hooks
- Prefer named exports
- Error messages should be user-friendly
```

---

## Guide — Table of Contents

### Getting Started
- [01 - Getting Started with Claude](guide/en/01-getting-started.md) — Installation, setup, and your first conversation

### Claude Code Mastery
- [02 - Claude Code Mastery](guide/en/02-claude-code-mastery.md) — Deep dive into Claude Code CLI features and workflows
- [03 - CLAUDE.md Guide](guide/en/03-claude-md-guide.md) — Best practices for project-level configuration
- [04 - Hooks & Automation](guide/en/04-hooks-and-automation.md) — Automate workflows with hooks and shell integration
- [05 - MCP Servers](guide/en/05-mcp-servers.md) — Extend Claude's capabilities with Model Context Protocol
- [06 - Multi-Agent Patterns](guide/en/06-multi-agent.md) — Orchestrate multiple Claude agents for complex tasks

### API & SDK
- [07 - API & SDK](guide/en/07-api-and-sdk.md) — Build applications with Claude API and Anthropic SDK
- [08 - Agent SDK](guide/en/08-agent-sdk.md) — Build custom agents with Claude Agent SDK

### Prompt Engineering
- [09 - Prompt Engineering](guide/en/09-prompt-engineering.md) — Techniques for getting the best results from Claude
- [10 - Advanced Workflows](guide/en/10-advanced-workflows.md) — Complex real-world automation patterns

### Production & Operations 🆕
- [11 - End-to-End Project](guide/en/11-end-to-end-project.md) — Build a complete app from idea to deployment with AI
- [12 - CI/CD Integration](guide/en/12-cicd-integration.md) — AI-powered code review, testing, and deployment pipelines
- [13 - Cost & Model Selection](guide/en/13-cost-and-model-selection.md) — Opus vs Sonnet vs Haiku, token budgeting, cost saving
- [14 - Debugging AI Code](guide/en/14-debugging-ai-code.md) — When AI gets it wrong: detection, recovery, prevention

### Team & Enterprise 🆕
- [15 - Team Workflows](guide/en/15-team-workflows.md) — Multi-person + AI collaboration, PR processes, onboarding
- [16 - Security & Compliance](guide/en/16-security-compliance.md) — Secrets management, OWASP, audit logging, compliance
- [17 - Large Codebase Management](guide/en/17-large-codebase.md) — 100K+ LOC projects, context strategies, monorepo patterns

---

## Templates

Ready-to-use templates — copy them directly into your projects:

| Template | Description |
|----------|-------------|
| [CLAUDE.md](templates/CLAUDE.md) | Universal project configuration template |
| [CLAUDE-python.md](templates/CLAUDE-python.md) | Python project template |
| [CLAUDE-typescript.md](templates/CLAUDE-typescript.md) | TypeScript/Node.js project template |
| [CLAUDE-rust.md](templates/CLAUDE-rust.md) | Rust project template |
| [CLAUDE-cpp.md](templates/CLAUDE-cpp.md) | C++ project template (CMake, GTest, clang-tidy) 🆕 |
| [CLAUDE-java.md](templates/CLAUDE-java.md) | Java project template (Spring Boot, Maven, JUnit 5) 🆕 |
| [CLAUDE-fullstack.md](templates/CLAUDE-fullstack.md) | Full-stack project template (frontend + backend + DB) 🆕 |
| [System Prompts](templates/system-prompts/) | Prompts for code review, writing, analysis, etc. |
| [Hook Scripts](templates/hooks/) | Pre-commit linting, auto-testing, and more |
| [Security Templates](templates/security/) | Security hooks, OWASP checklist for AI code 🆕 |

---

## Examples

Runnable code samples organized by category:

### Full-Stack Demo 🆕
- [Task Manager Demo](examples/fullstack-demo/) — Complete project with CLAUDE.md + hooks + CI/CD + Docker

### CI/CD Templates 🆕
- [AI Code Review](examples/cicd-templates/github-actions/ai-code-review.yml) — GitHub Actions: AI reviews every PR
- [AI Test Generation](examples/cicd-templates/github-actions/ai-test-gen.yml) — Auto-generate tests for changed files
- [GitLab CI](examples/cicd-templates/gitlab-ci/) — GitLab equivalent pipelines

### Claude Code
- [Hook configurations](examples/claude-code/hooks/) — Custom hooks for automation
- [MCP server configs](examples/claude-code/mcp-configs/) — Ready-to-use MCP setups
- [CLAUDE.md examples](examples/claude-code/claude-md/) — Real project configurations

### API & SDK
- [Tool Use patterns](examples/api/tool-use/) — Function calling and tool integration
- [Streaming](examples/api/streaming/) — Real-time streaming responses

### Agents
- [Simple Agent](examples/agents/simple-agent/) — Basic agent with tools
- [Code Review Bot](examples/agents/code-review-bot/) — Practical automated code reviewer

### AI Coding Workflow Frameworks / AI 编码工作流框架 🆕

> Harness frameworks that turn AI coding into structured engineering workflows: requirements → design → implement → review → ship.
>
> 将 AI 编码变成结构化工程流程的 Harness 框架：需求→设计→实现→审查→交付。

| Category / 分类 | Frameworks / 框架 |
|-----------------|-------------------|
| Methodology / 方法论 | [Superpowers](examples/frameworks/superpowers/) · [GSD](examples/frameworks/gsd/) · [Spec-Kit](examples/frameworks/spec-kit/) · [BMAD](examples/frameworks/bmad-method/) |
| Virtual Team / 虚拟团队 | [GStack](examples/frameworks/gstack/) · [ECC](examples/frameworks/ecc/) |
| Orchestration / 编排进化 | [Hermes Agent](examples/frameworks/hermes-agent/) · [Citadel](examples/frameworks/citadel/) |
| Full Lifecycle / 全生命周期 | [CC Harness](examples/frameworks/claude-code-harness/) · [CC Workflows](examples/frameworks/claude-code-workflows/) |

👉 **[Full Guide with Comparisons / 完整指南与对比 →](examples/frameworks/)**

---

## Awesome Resources

> Full list: [awesome.md](awesome.md)

### Official
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic's official CLI for Claude
- [Anthropic SDK (Python)](https://github.com/anthropics/anthropic-sdk-python) — Official Python SDK
- [Anthropic SDK (TypeScript)](https://github.com/anthropics/anthropic-sdk-typescript) — Official TypeScript SDK
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) — Build custom agents
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — Official code examples

---

## Contributing

Contributions are welcome! Whether it's fixing a typo, adding a new template, or writing a guide — every contribution helps.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <sub>If you find this useful, please give it a star! It helps others discover this resource.</sub>
</p>
