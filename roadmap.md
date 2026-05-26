# Claude Mastery Roadmap / Claude 学习路线图

> Your path from beginner to Claude expert. Follow the stages in order, or jump to what you need.
>
> 从入门到精通的完整路径。按顺序学习，或直接跳到你需要的部分。

---

## Overview / 总览

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      CLAUDE MASTERY ROADMAP                             ║
╚══════════════════════════════════════════════════════════════════════════╝

 ┌─────────────────────────────────────────────────────────────────────────┐
 │                                                                         │
 │  STAGE 1: Getting Started / 入门                       [Ch 01]          │
 │  ───────────────────────────────                                        │
 │  Install → First Chat → /init & CLAUDE.md                               │
 │                                                                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │                                                                         │
 │  STAGE 2: Claude Code Mastery / CLI 精通               [Ch 02-06]       │
 │  ───────────────────────────────────────                                │
 │  Interactive → Plan Mode → Git → Pipes → /compact                       │
 │  CLAUDE.md → Hooks → MCP → Multi-Agent                                 │
 │                                                                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │                                                                         │
 │  STAGE 3: API & SDK / 编程接入                         [Ch 07-08]       │
 │  ─────────────────────────────                                          │
 │  Claude API → Tool Use → Streaming → Agent SDK                          │
 │                                                                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │                                                                         │
 │  STAGE 4: Prompt & Advanced / 工程进阶                 [Ch 09-10]       │
 │  ─────────────────────────────────────                                  │
 │  Prompt Engineering → Advanced Workflows → CI/CD Patterns               │
 │                                                                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │                                                                         │
 │  STAGE 5: Production / 生产与运维                      [Ch 11-14]       │
 │  ────────────────────────────────                                       │
 │  End-to-End Project → CI/CD → Cost Control → Debug AI Code              │
 │                                                                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │                                                                         │
 │  STAGE 6: Team & Enterprise / 团队与企业               [Ch 15-17]       │
 │  ──────────────────────────────────────                                 │
 │  Team Workflows → Security & Compliance → Large Codebase                │
 │                                                                         │
 └─────────────────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Getting Started / 入门

> **Goal / 目标**: Install Claude Code and have your first productive conversation.
> 安装 Claude Code 并完成你的第一次有效对话。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 1.1 | Install Claude Code | [Getting Started](guide/en/01-getting-started.md) / [入门指南](guide/zh/01-getting-started.md) | 安装 CLI 并配置 API 密钥 |
| 1.2 | First conversation | [Getting Started](guide/en/01-getting-started.md#your-first-session) | 启动交互式会话，试几个命令 |
| 1.3 | Create CLAUDE.md | [CLAUDE.md Guide](guide/en/03-claude-md-guide.md) / [CLAUDE.md 指南](guide/zh/03-claude-md-guide.md) | 运行 `/init`，为项目生成配置 |

**Checkpoint / 检查点**: You can start Claude Code, ask questions about your project, and have a `CLAUDE.md` file.
能启动 Claude Code，询问项目相关问题，项目中有 `CLAUDE.md` 文件。

---

## Stage 2: Claude Code Mastery / CLI 精通

> **Goal / 目标**: Master Claude Code's features for everyday development.
> 精通 Claude Code 的各项功能，将其用于日常开发。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 2.1 | Interactive workflows | [CLI Mastery](guide/en/02-claude-code-mastery.md) / [精通指南](guide/zh/02-claude-code-mastery.md) | 交互模式、Plan 模式、Git 工作流 |
| 2.2 | Non-interactive & pipes | [CLI Mastery](guide/en/02-claude-code-mastery.md#non-interactive-mode) | `claude -p` 做脚本和管道 |
| 2.3 | CLAUDE.md deep dive | [CLAUDE.md Guide](guide/en/03-claude-md-guide.md) / [CLAUDE.md 指南](guide/zh/03-claude-md-guide.md) | 多层级配置、上下文工程 |
| 2.4 | Hooks & automation | [Hooks](guide/en/04-hooks-and-automation.md) / [Hooks 与自动化](guide/zh/04-hooks-and-automation.md) | 自动 lint、测试、通知 |
| 2.5 | MCP servers | [MCP](guide/en/05-mcp-servers.md) / [MCP 服务器](guide/zh/05-mcp-servers.md) | 连接数据库、GitHub、浏览器 |
| 2.6 | Multi-agent patterns | [Multi-Agent](guide/en/06-multi-agent.md) / [多 Agent](guide/zh/06-multi-agent.md) | 子 Agent、并行执行 |

**Checkpoint / 检查点**: You use Claude Code daily with hooks, MCP, and multi-agent. You know Plan mode vs. direct execution.
日常使用 Claude Code，配置了 Hooks 和 MCP，掌握 Plan 模式。

---

## Stage 3: API & SDK / 编程接入

> **Goal / 目标**: Build applications with Claude API and create custom agents.
> 用 Claude API 构建应用、创建自定义 Agent。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 3.1 | Claude API & SDK | [API & SDK](guide/en/07-api-and-sdk.md) / [API 与 SDK](guide/zh/07-api-and-sdk.md) | Messages API、Tool Use、流式响应 |
| 3.2 | Agent SDK | [Agent SDK](guide/en/08-agent-sdk.md) / [Agent SDK](guide/zh/08-agent-sdk.md) | 构建带工具和护栏的自定义 Agent |

**Checkpoint / 检查点**: You can call Claude API from code, use tool calling, and build custom agents.
能用代码调用 Claude API、使用 Tool Use、构建自定义 Agent。

---

## Stage 4: Prompt & Advanced / 工程进阶

> **Goal / 目标**: Master prompt engineering and complex automation patterns.
> 精通 Prompt 工程和复杂自动化模式。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 4.1 | Prompt engineering | [Prompt Engineering](guide/en/09-prompt-engineering.md) / [Prompt 工程](guide/zh/09-prompt-engineering.md) | XML 标签、Few-shot、系统提示 |
| 4.2 | Advanced workflows | [Advanced Workflows](guide/en/10-advanced-workflows.md) / [高级工作流](guide/zh/10-advanced-workflows.md) | 自动审查、测试生成、发布管理 |

**Checkpoint / 检查点**: Your prompts consistently produce excellent results. You've built automated review and testing workflows.
Prompt 能持续产出优秀结果，已搭建自动化审查和测试工作流。

---

## Stage 5: Production / 生产与运维

> **Goal / 目标**: Ship AI-assisted code to production with confidence.
> 自信地将 AI 辅助代码交付到生产环境。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 5.1 | End-to-end project | [E2E Project](guide/en/11-end-to-end-project.md) / [端到端实战](guide/zh/11-end-to-end-project.md) | 从想法到部署的完整项目 |
| 5.2 | CI/CD integration | [CI/CD](guide/en/12-cicd-integration.md) / [CI/CD 集成](guide/zh/12-cicd-integration.md) | AI 审查 PR、生成测试、安全扫描 |
| 5.3 | Cost & model selection | [Cost](guide/en/13-cost-and-model-selection.md) / [成本与模型](guide/zh/13-cost-and-model-selection.md) | Opus/Sonnet/Haiku 选择、Token 省钱 |
| 5.4 | Debugging AI code | [Debugging](guide/en/14-debugging-ai-code.md) / [调试 AI 代码](guide/zh/14-debugging-ai-code.md) | 幻觉、回滚、预防模式 |

**Checkpoint / 检查点**: You can deliver complete projects, run AI-powered CI/CD, and manage costs effectively.
能端到端交付完整项目、运行 AI 驱动的 CI/CD、有效控制成本。

---

## Stage 6: Team & Enterprise / 团队与企业

> **Goal / 目标**: Scale AI-assisted development across teams with proper governance.
> 在团队中规模化推广 AI 辅助开发，确保安全合规。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 6.1 | Team workflows | [Teams](guide/en/15-team-workflows.md) / [团队协作](guide/zh/15-team-workflows.md) | 多人+AI 协作、PR 流程、入职 |
| 6.2 | Security & compliance | [Security](guide/en/16-security-compliance.md) / [安全合规](guide/zh/16-security-compliance.md) | Secrets、OWASP、审计、合规 |
| 6.3 | Large codebase | [Large Codebase](guide/en/17-large-codebase.md) / [大项目管理](guide/zh/17-large-codebase.md) | 10万行代码的上下文策略 |

**Checkpoint / 检查点**: Your team collaborates effectively with AI, passes security audits, and handles large codebases.
团队高效地与 AI 协作、通过安全审计、管理大型代码库。

---

## Quick Reference / 快速参考

Not sure where to start? Here's a guide based on your role:

不确定从哪开始？根据你的角色参考：

| Role / 角色 | Start At / 从这里开始 | Focus / 重点 |
|-------------|----------------------|--------------|
| **Beginner / 初学者** | Stage 1 | 先跑起来，用 /init 生成 CLAUDE.md |
| **Developer / 开发者** | Stage 2 | CLI 精通、Hooks、MCP |
| **API Builder / API 开发者** | Stage 3 | Claude API、Agent SDK |
| **Power User / 高级用户** | Stage 4 | Prompt 工程、高级自动化 |
| **Shipping to Prod / 上线交付** | Stage 5 | 端到端实战、CI/CD、成本控制 |
| **Tech Lead / 技术负责人** | Stage 6 | 团队协作、安全合规、大项目管理 |

---

## Resources / 资源

| Resource | Link | 说明 |
|----------|------|------|
| Cheatsheet (EN) | [cheatsheet.md](cheatsheet.md) | 英文命令速查表 |
| 中文速查表 | [cheatsheet_zh.md](cheatsheet_zh.md) | 中文命令速查表 |
| 工具对比 | [comparison.md](comparison.md) | Claude Code vs Cursor vs Copilot vs Windsurf |
| 知识总览 | [overview.md](overview.md) | 一页纸知识地图 |
| Templates | [templates/](templates/) | 即用模板 |
| Examples | [examples/](examples/) | 可运行代码示例 |
| Awesome List | [awesome.md](awesome.md) | 精选资源聚合 |

---

<p align="center">
  <sub>Part of <a href="README.md">claude-engineer</a> — star this repo to bookmark your learning journey!</sub>
</p>
