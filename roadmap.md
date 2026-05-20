# Claude Mastery Roadmap / Claude 学习路线图

> Your path from beginner to Claude expert. Follow the stages in order, or jump to what you need.
>
> 从入门到精通的完整路径。按顺序学习，或直接跳到你需要的部分。

---

## Overview / 总览

```
                        ╔══════════════════════════════════════╗
                        ║      CLAUDE MASTERY ROADMAP          ║
                        ╚══════════════════════════════════════╝

 ┌─────────────────────────────────────────────────────────────────────────┐
 │                                                                         │
 │  🟢 STAGE 1: Getting Started / 入门                                     │
 │  ─────────────────────────────────────                                  │
 │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
 │  │ Install      │─►│ First Chat   │─►│ /init &      │                  │
 │  │ Claude Code  │  │ with Claude  │  │ CLAUDE.md    │                  │
 │  └──────────────┘  └──────────────┘  └──────┬───────┘                  │
 │                                              │                          │
 ├──────────────────────────────────────────────┼──────────────────────────┤
 │                                              ▼                          │
 │  🔵 STAGE 2: Daily Driver / 日常使用                                    │
 │  ─────────────────────────────────────                                  │
 │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
 │  │ Interactive   │─►│ Plan Mode    │─►│ Git &        │                  │
 │  │ Workflows    │  │ (Shift+Tab)  │  │ PR Workflow  │                  │
 │  └──────────────┘  └──────────────┘  └──────────────┘                  │
 │         │                                                               │
 │         ▼                                                               │
 │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
 │  │ Non-         │─►│ Pipe &       │─►│ Context &    │                  │
 │  │ Interactive  │  │ Chain Cmds   │  │ /compact     │                  │
 │  └──────────────┘  └──────────────┘  └──────┬───────┘                  │
 │                                              │                          │
 ├──────────────────────────────────────────────┼──────────────────────────┤
 │                                              ▼                          │
 │  🟡 STAGE 3: Power User / 高级用户                                      │
 │  ─────────────────────────────────────                                  │
 │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
 │  │ Hooks &      │─►│ MCP          │─►│ Prompt       │                  │
 │  │ Automation   │  │ Servers      │  │ Engineering  │                  │
 │  └──────────────┘  └──────────────┘  └──────────────┘                  │
 │         │                                                               │
 │         ▼                                                               │
 │  ┌──────────────┐  ┌──────────────┐                                    │
 │  │ Permissions  │─►│ Custom       │                                    │
 │  │ & Settings   │  │ Templates    │                                    │
 │  └──────────────┘  └──────┬───────┘                                    │
 │                            │                                            │
 ├────────────────────────────┼────────────────────────────────────────────┤
 │                            ▼                                            │
 │  🔴 STAGE 4: Expert / 专家                                              │
 │  ─────────────────────────────────────                                  │
 │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
 │  │ Claude API   │─►│ Agent SDK    │─►│ Multi-Agent  │                  │
 │  │ & SDK        │  │              │  │ Patterns     │                  │
 │  └──────────────┘  └──────────────┘  └──────────────┘                  │
 │         │                                                               │
 │         ▼                                                               │
 │  ┌──────────────┐  ┌──────────────┐                                    │
 │  │ CI/CD        │─►│ Custom MCP   │                                    │
 │  │ Integration  │  │ Servers      │                                    │
 │  └──────────────┘  └──────────────┘                                    │
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

## Stage 2: Daily Driver / 日常使用

> **Goal / 目标**: Use Claude Code efficiently for everyday development tasks.
> 高效地将 Claude Code 用于日常开发任务。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 2.1 | Interactive workflows | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#interactive-mode) / [精通指南](guide/zh/02-claude-code-mastery.md) | 掌握交互模式的有效提示 |
| 2.2 | Plan mode | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#plan-mode) | 用 Shift+Tab 先规划再执行 |
| 2.3 | Non-interactive mode | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#non-interactive-mode) | 用 `claude -p` 做脚本和管道 |
| 2.4 | Git workflows | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#working-with-git) | Commit、PR、代码审查 |
| 2.5 | Context management | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#context-management) | 掌握 `/compact`、多目录上下文 |
| 2.6 | Writing tests | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#working-with-tests) | TDD、测试生成、覆盖率 |

**Checkpoint / 检查点**: You use Claude Code daily for coding, reviews, and git operations. You know when to use Plan mode vs. direct execution.
日常使用 Claude Code 编码、审查和 Git 操作。知道何时使用 Plan 模式。

---

## Stage 3: Power User / 高级用户

> **Goal / 目标**: Automate workflows, extend Claude's capabilities, and master prompt engineering.
> 自动化工作流，扩展 Claude 能力，精通 Prompt 工程。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 3.1 | Hooks | [Hooks & Automation](guide/en/04-hooks-and-automation.md) / [Hooks 与自动化](guide/zh/04-hooks-and-automation.md) | 自动 lint、测试、通知 |
| 3.2 | MCP Servers | [MCP Servers](guide/en/05-mcp-servers.md) / [MCP 服务器](guide/zh/05-mcp-servers.md) | 连接数据库、GitHub、浏览器 |
| 3.3 | Prompt engineering | [Prompt Engineering](guide/en/09-prompt-engineering.md) / [Prompt 工程](guide/zh/09-prompt-engineering.md) | XML 标签、Few-shot、系统提示 |
| 3.4 | Advanced CLAUDE.md | [CLAUDE.md Guide](guide/en/03-claude-md-guide.md#advanced-patterns) | 条件指令、按目录配置 |
| 3.5 | Permissions & settings | [Claude Code Mastery](guide/en/02-claude-code-mastery.md#permission-system) | 精细化权限控制 |
| 3.6 | Templates | [Templates](templates/) | 使用和定制即用模板 |

**Checkpoint / 检查点**: Your workflow is automated with hooks, Claude can access databases and APIs via MCP, and your prompts consistently produce excellent results.
工作流已通过 Hooks 自动化，Claude 可通过 MCP 访问数据库和 API，Prompt 能持续产出优秀结果。

---

## Stage 4: Expert / 专家

> **Goal / 目标**: Build applications with Claude API, create custom agents, and design complex multi-agent systems.
> 用 Claude API 构建应用、创建自定义 Agent、设计复杂的多 Agent 系统。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 4.1 | Claude API & SDK | [API & SDK](guide/en/07-api-and-sdk.md) / [API 与 SDK](guide/zh/07-api-and-sdk.md) | Messages API、Tool Use、流式响应 |
| 4.2 | Agent SDK | [Agent SDK](guide/en/08-agent-sdk.md) / [Agent SDK](guide/zh/08-agent-sdk.md) | 构建带工具和护栏的 Agent |
| 4.3 | Multi-agent patterns | [Multi-Agent](guide/en/06-multi-agent.md) / [多 Agent](guide/zh/06-multi-agent.md) | 扇出/扇入、流水线、路由 |
| 4.4 | CI/CD integration | [Advanced Workflows](guide/en/10-advanced-workflows.md) / [高级工作流](guide/zh/10-advanced-workflows.md) | GitHub Actions、自动审查 |
| 4.5 | Custom MCP servers | [MCP Servers](guide/en/05-mcp-servers.md#building-custom-mcp-servers) | 构建自定义工具服务器 |

**Checkpoint / 检查点**: You can build production applications powered by Claude, orchestrate multi-agent systems, and integrate Claude into CI/CD pipelines.
能构建 Claude 驱动的生产应用、编排多 Agent 系统、将 Claude 集成到 CI/CD 流水线。

---

## Stage 5: Production / 生产落地 🆕

> **Goal / 目标**: Ship AI-assisted code to production with confidence — end-to-end projects, CI/CD, cost control, team workflows, security, and large codebase management.
> 自信地将 AI 辅助代码交付到生产环境——端到端项目、CI/CD、成本控制、团队协作、安全和大项目管理。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 5.1 | End-to-end project | [E2E Project](guide/en/11-end-to-end-project.md) / [端到端实战](guide/zh/11-end-to-end-project.md) | 从想法到部署的完整项目 |
| 5.2 | CI/CD integration | [CI/CD](guide/en/12-cicd-integration.md) / [CI/CD 集成](guide/zh/12-cicd-integration.md) | AI 审查 PR、生成测试、安全扫描 |
| 5.3 | Cost & model selection | [Cost](guide/en/13-cost-and-model-selection.md) / [成本与模型](guide/zh/13-cost-and-model-selection.md) | Opus/Sonnet/Haiku 选择、Token 省钱 |
| 5.4 | Debugging AI code | [Debugging](guide/en/14-debugging-ai-code.md) / [调试 AI 代码](guide/zh/14-debugging-ai-code.md) | 幻觉、回滚、预防模式 |
| 5.5 | Team workflows | [Teams](guide/en/15-team-workflows.md) / [团队协作](guide/zh/15-team-workflows.md) | 多人+AI 协作、PR 流程、入职 |
| 5.6 | Security & compliance | [Security](guide/en/16-security-compliance.md) / [安全合规](guide/zh/16-security-compliance.md) | Secrets、OWASP、审计、合规 |
| 5.7 | Large codebase | [Large Codebase](guide/en/17-large-codebase.md) / [大项目管理](guide/zh/17-large-codebase.md) | 10万行代码的上下文策略 |

**Checkpoint / 检查点**: You can deliver complete projects end-to-end with AI, run AI-powered CI/CD pipelines, manage costs, work in teams, pass security audits, and handle large codebases.
能端到端交付完整项目、运行 AI 驱动的 CI/CD、控制成本、团队协作、通过安全审计、管理大型代码库。

---

## Quick Reference / 快速参考

Not sure where to start? Here's a guide based on your role:

不确定从哪开始？根据你的角色参考：

| Role / 角色 | Start At / 从这里开始 | Focus / 重点 |
|-------------|----------------------|--------------|
| **Beginner / 初学者** | Stage 1 | 先跑起来，用 /init 生成 CLAUDE.md |
| **Developer / 开发者** | Stage 2 | 日常编码、测试、Git 工作流 |
| **Team Lead / 技术主管** | Stage 3 | Hooks 自动化、权限、模板标准化 |
| **Platform Engineer / 平台工程师** | Stage 4 | API 集成、Agent SDK、CI/CD |
| **AI Builder / AI 应用开发者** | Stage 4 | Agent SDK、Multi-Agent、Tool Use |
| **Tech Lead / 技术负责人** | Stage 5 | 团队协作、安全合规、大项目管理 |
| **Shipping to Production / 上线交付** | Stage 5 | 端到端实战、CI/CD、成本控制 |

---

## Resources / 资源

| Resource | Link | 说明 |
|----------|------|------|
| Cheatsheet | [cheatsheet.md](cheatsheet.md) | 命令速查表 |
| Templates | [templates/](templates/) | 即用模板 |
| Examples | [examples/](examples/) | 可运行代码示例 |
| Awesome List | [awesome.md](awesome.md) | 精选资源聚合 |

---

<p align="center">
  <sub>Part of <a href="README.md">claude-engineer</a> — star this repo to bookmark your learning journey!</sub>
</p>
