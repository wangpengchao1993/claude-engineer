<p align="center">
  <img src="assets/banner.png" alt="Claude Engineer Banner" width="800">
</p>

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

---

## Templates

Ready-to-use templates — copy them directly into your projects:

| Template | Description |
|----------|-------------|
| [CLAUDE.md](templates/CLAUDE.md) | Universal project configuration template |
| [CLAUDE-python.md](templates/CLAUDE-python.md) | Python project template |
| [CLAUDE-typescript.md](templates/CLAUDE-typescript.md) | TypeScript/Node.js project template |
| [CLAUDE-rust.md](templates/CLAUDE-rust.md) | Rust project template |
| [System Prompts](templates/system-prompts/) | Prompts for code review, writing, analysis, etc. |
| [Hook Scripts](templates/hooks/) | Pre-commit linting, auto-testing, and more |

---

## Examples

Runnable code samples organized by category:

### Claude Code
- [Hook configurations](examples/claude-code/hooks/) — Custom hooks for automation
- [MCP server configs](examples/claude-code/mcp-configs/) — Ready-to-use MCP setups
- [CLAUDE.md examples](examples/claude-code/claude-md/) — Real project configurations

### API & SDK
- [Tool Use patterns](examples/api/tool-use/) — Function calling and tool integration
- [Streaming](examples/api/streaming/) — Real-time streaming responses
- [Multimodal](examples/api/multimodal/) — Image and PDF processing

### Agents
- [Simple Agent](examples/agents/simple-agent/) — Basic agent with tools
- [Multi-Agent](examples/agents/multi-agent/) — Agent orchestration patterns
- [Code Review Bot](examples/agents/code-review-bot/) — Practical automated code reviewer

### AI Frameworks Guide / AI 框架指南 🆕

> Beginner-friendly introductions to 10 popular AI frameworks, each with runnable examples and tests.
>
> 面向小白的 10 大主流 AI 框架介绍，每个都有可运行示例和测试。

| Category / 分类 | Frameworks / 框架 |
|-----------------|-------------------|
| LLM Apps / 大模型应用 | [LangChain](examples/frameworks/langchain/) · [LlamaIndex](examples/frameworks/llamaindex/) |
| Agents / 智能体 | [CrewAI](examples/frameworks/crewai/) · [LangGraph](examples/frameworks/langgraph/) · [OpenAI Agents](examples/frameworks/openai-agents/) |
| Prompt Optimization / 提示词优化 | [DSPy](examples/frameworks/dspy/) |
| Model Serving / 模型部署 | [Ollama](examples/frameworks/ollama/) · [LiteLLM](examples/frameworks/litellm/) |
| Evaluation / 评估测试 | [DeepEval](examples/frameworks/deepeval/) |
| Models & Fine-tuning / 模型微调 | [Hugging Face](examples/frameworks/huggingface/) |

👉 **[Full Guide / 完整指南 →](examples/frameworks/)**

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
