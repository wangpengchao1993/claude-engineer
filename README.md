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

## Where to Start?

| I want to... | Go here |
|--------------|---------|
| See the big picture | [Knowledge Map](overview.md) |
| Follow a learning path from zero | [Roadmap](roadmap.md) → [Chapter 01: Getting Started](guide/en/01-getting-started.md) |
| Look up a command / shortcut / API param | [Cheatsheet](cheatsheet.md) · [中文速查表](cheatsheet_zh.md) |
| Compare Claude Code with other tools | [Tool Comparison](comparison.md) |
| Copy a project template | [Templates](templates/) — Python · C++ · Java · TS · Rust · Fullstack |
| Build a complete project with AI | [Chapter 11: End-to-End Project](guide/en/11-end-to-end-project.md) |
| Set up AI CI/CD pipelines | [Chapter 12: CI/CD Integration](guide/en/12-cicd-integration.md) |
| Save money on tokens | [Chapter 13: Cost & Model Selection](guide/en/13-cost-and-model-selection.md) |
| Find tools, libraries, and articles | [Awesome Resources](awesome.md) |

---

## Learning Roadmap

> Full roadmap: [roadmap.md](roadmap.md)

```
Stage 1: Getting Started    Stage 2: CLI Mastery        Stage 3: API & SDK
  Install → First Chat →      Interactive/Plan →           Claude API →
  /init & CLAUDE.md            Hooks → MCP → Multi-Agent    Tool Use → Agent SDK

Stage 4: Prompt & Advanced  Stage 5: Production         Stage 6: Team & Enterprise
  Prompt Engineering →         E2E Project → CI/CD →       Team Workflows →
  Advanced Workflows           Cost Control → Debug AI      Security → Large Codebase
```

---

## Guide — Table of Contents (17 Chapters)

Chapters are ordered from beginner to advanced. Recommended to read in order.

### Stage 1: Getting Started

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| [01](guide/en/01-getting-started.md) | Getting Started | Installation, setup, first conversation |

### Stage 2: Claude Code Mastery

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| [02](guide/en/02-claude-code-mastery.md) | CLI Mastery | Interactive/non-interactive modes, pipes, Plan mode |
| [03](guide/en/03-claude-md-guide.md) | CLAUDE.md Guide | Project config, context engineering, multi-level rules |
| [04](guide/en/04-hooks-and-automation.md) | Hooks & Automation | Event hooks, auto-lint, quality guardrails |
| [05](guide/en/05-mcp-servers.md) | MCP Servers | Extend Claude's tool capabilities |
| [06](guide/en/06-multi-agent.md) | Multi-Agent Patterns | Subagents, parallel execution, orchestration |

### Stage 3: API & SDK

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| [07](guide/en/07-api-and-sdk.md) | API & SDK | Call Claude from code (Python/TypeScript) |
| [08](guide/en/08-agent-sdk.md) | Agent SDK | Build custom agents |

### Stage 4: Prompt & Advanced

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| [09](guide/en/09-prompt-engineering.md) | Prompt Engineering | Structured prompts, Claude-specific techniques |
| [10](guide/en/10-advanced-workflows.md) | Advanced Workflows | Automated review, test gen, release management |

### Stage 5: Production

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| [11](guide/en/11-end-to-end-project.md) | End-to-End Project | Full AI dev flow from idea to deployment |
| [12](guide/en/12-cicd-integration.md) | CI/CD Integration | AI-powered code review and deployment pipelines |
| [13](guide/en/13-cost-and-model-selection.md) | Cost & Model Selection | Opus/Sonnet/Haiku comparison, cost saving |
| [14](guide/en/14-debugging-ai-code.md) | Debugging AI Code | Common AI errors, prevention and recovery |

### Stage 6: Team & Enterprise

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| [15](guide/en/15-team-workflows.md) | Team Workflows | Multi-person + AI collaboration, PR processes |
| [16](guide/en/16-security-compliance.md) | Security & Compliance | Secrets, OWASP, audit logging, compliance |
| [17](guide/en/17-large-codebase.md) | Large Codebase | 100K+ LOC context strategies, monorepo patterns |

---

## Templates

Ready-to-use templates — copy them directly into your projects:

| Template | Description |
|----------|-------------|
| [CLAUDE.md](templates/CLAUDE.md) | Universal project configuration template |
| [CLAUDE-python.md](templates/CLAUDE-python.md) | Python project template |
| [CLAUDE-typescript.md](templates/CLAUDE-typescript.md) | TypeScript/Node.js project template |
| [CLAUDE-rust.md](templates/CLAUDE-rust.md) | Rust project template |
| [CLAUDE-cpp.md](templates/CLAUDE-cpp.md) | C++ project template (CMake, GTest, clang-tidy) |
| [CLAUDE-java.md](templates/CLAUDE-java.md) | Java project template (Spring Boot, Maven, JUnit 5) |
| [CLAUDE-fullstack.md](templates/CLAUDE-fullstack.md) | Full-stack project template (frontend + backend + DB) |
| [System Prompts](templates/system-prompts/) | Prompts for code review, writing, analysis, etc. |
| [Hook Scripts](templates/hooks/) | Pre-commit linting, auto-testing, and more |
| [Security Templates](templates/security/) | Security hooks, OWASP checklist for AI code |

---

## Examples

Runnable code samples organized by category:

### Full-Stack Demo
- [Task Manager Demo](examples/fullstack-demo/) — Complete project with CLAUDE.md + hooks + CI/CD + Docker

### CI/CD Templates
- [AI Code Review](examples/cicd-templates/github-actions/ai-code-review.yml) — GitHub Actions: AI reviews every PR
- [AI Test Generation](examples/cicd-templates/github-actions/ai-test-gen.yml) — Auto-generate tests for changed files
- [GitLab CI](examples/cicd-templates/gitlab-ci/) — GitLab equivalent pipelines

### Claude Code Config
- [Hook configurations](examples/claude-code/hooks/) — Custom hooks for automation
- [MCP server configs](examples/claude-code/mcp-configs/) — Ready-to-use MCP setups
- [CLAUDE.md examples](examples/claude-code/claude-md/) — Real project configurations

### API & SDK
- [Tool Use patterns](examples/api/tool-use/) — Function calling and tool integration
- [Streaming](examples/api/streaming/) — Real-time streaming responses

### Agents
- [Simple Agent](examples/agents/simple-agent/) — Basic agent with tools
- [Code Review Bot](examples/agents/code-review-bot/) — Practical automated code reviewer

### Workflow Frameworks

> Frameworks that turn AI coding into structured engineering workflows: requirements → design → implement → review → ship.

| Category | Frameworks |
|----------|-----------|
| Methodology | [Superpowers](examples/frameworks/superpowers/) · [GSD](examples/frameworks/gsd/) · [Spec-Kit](examples/frameworks/spec-kit/) · [BMAD](examples/frameworks/bmad-method/) |
| Virtual Team | [GStack](examples/frameworks/gstack/) · [ECC](examples/frameworks/ecc/) |
| Orchestration | [Hermes Agent](examples/frameworks/hermes-agent/) · [Citadel](examples/frameworks/citadel/) |
| Full Lifecycle | [CC Harness](examples/frameworks/claude-code-harness/) · [CC Workflows](examples/frameworks/claude-code-workflows/) |

👉 **[Full Guide with Comparisons →](examples/frameworks/)**

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
