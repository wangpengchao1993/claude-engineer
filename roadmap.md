# Claude Engineer 知识体系与学习路线

> 一张图看懂全貌，六个阶段从入门到精通。
>
> One map to see the big picture, six stages from beginner to expert.

---

## 知识地图 / Knowledge Map

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    CLAUDE ENGINEER 知识体系                             ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     认知层 / MINDSET                              │  │
│  │                                                                   │  │
│  │  "AI 不是替代你，而是放大你"                                       │  │
│  │                                                                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │  │
│  │  │ Human-AI     │  │ Context      │  │ AI-Native            │    │  │
│  │  │ 协作模型     │  │ Engineering  │  │ 开发方法论           │    │  │
│  │  │              │  │              │  │                      │    │  │
│  │  │ · AI 擅长/短板│  │ · 上下文设计 │  │ · Spec-first         │    │  │
│  │  │ · 信任校准   │  │ · 预算分配   │  │ · 迭代粒度           │    │  │
│  │  │ · L1→L5 类比 │  │ · 信息密度   │  │ · AI-Driven TDD      │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     工具层 / TOOLS                                │  │
│  │                                                                   │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │              Claude Code（CLI + 桌面 + Web + IDE）        │    │  │
│  │  │  交互模式 · 非交互模式 · 管道 · Plan模式 · /compact       │    │  │
│  │  └──────────────────────┬───────────────────────────────────┘    │  │
│  │           ┌─────────────┼─────────────┐                          │  │
│  │           ▼             ▼             ▼                          │  │
│  │  ┌──────────────┐ ┌──────────┐ ┌──────────────┐                 │  │
│  │  │  CLAUDE.md   │ │  Hooks   │ │  MCP Servers │                 │  │
│  │  │  上下文工程  │ │  自动化  │ │  工具扩展    │                 │  │
│  │  └──────────────┘ └──────────┘ └──────────────┘                 │  │
│  │                                                                   │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │   Claude API & SDK · Agent SDK · 多 Agent 编排            │    │  │
│  │  └──────────────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     工程层 / ENGINEERING                          │  │
│  │                                                                   │  │
│  │  Prompt 工程 · 代码质量(Debug/AI债务) · 安全合规 · 大型代码库     │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                     落地层 / PRODUCTION                           │  │
│  │                                                                   │  │
│  │  端到端项目 · CI/CD · 成本控制 · 团队协作 · 工作流框架           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 学习路线 / Learning Path

### Stage 1: Getting Started / 入门

> 安装 Claude Code 并完成你的第一次有效对话。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 1.1 | Install Claude Code | [EN](guide/en/01-getting-started.md) / [中文](guide/zh/01-getting-started.md) | 安装 CLI 并配置 API 密钥 |
| 1.2 | First conversation | [EN](guide/en/01-getting-started.md#your-first-session) | 启动交互式会话 |
| 1.3 | Create CLAUDE.md | [EN](guide/en/03-claude-md-guide.md) / [中文](guide/zh/03-claude-md-guide.md) | 运行 `/init`，为项目生成配置 |

**检查点**: 能启动 Claude Code，项目中有 `CLAUDE.md` 文件。

---

### Stage 2: Claude Code Mastery / CLI 精通

> 精通 Claude Code 的各项功能，将其用于日常开发。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 2.1 | Interactive workflows | [EN](guide/en/02-claude-code-mastery.md) / [中文](guide/zh/02-claude-code-mastery.md) | 交互模式、Plan 模式、Git 工作流 |
| 2.2 | Non-interactive & pipes | [EN](guide/en/02-claude-code-mastery.md#non-interactive-mode) | `claude -p` 做脚本和管道 |
| 2.3 | CLAUDE.md deep dive | [EN](guide/en/03-claude-md-guide.md) / [中文](guide/zh/03-claude-md-guide.md) | 多层级配置、上下文工程 |
| 2.4 | Hooks & automation | [EN](guide/en/04-hooks-and-automation.md) / [中文](guide/zh/04-hooks-and-automation.md) | 自动 lint、测试、通知 |
| 2.5 | MCP servers | [EN](guide/en/05-mcp-servers.md) / [中文](guide/zh/05-mcp-servers.md) | 连接数据库、GitHub、浏览器 |
| 2.6 | Multi-agent patterns | [EN](guide/en/06-multi-agent.md) / [中文](guide/zh/06-multi-agent.md) | 子 Agent、并行执行 |

**检查点**: 日常使用 Claude Code，配置了 Hooks 和 MCP，掌握 Plan 模式。

---

### Stage 3: API & SDK / 编程接入

> 用 Claude API 构建应用、创建自定义 Agent。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 3.1 | Claude API & SDK | [EN](guide/en/07-api-and-sdk.md) / [中文](guide/zh/07-api-and-sdk.md) | Messages API、Tool Use、流式响应 |
| 3.2 | Agent SDK | [EN](guide/en/08-agent-sdk.md) / [中文](guide/zh/08-agent-sdk.md) | 构建带工具和护栏的自定义 Agent |

**检查点**: 能用代码调用 Claude API、使用 Tool Use、构建自定义 Agent。

---

### Stage 4: Prompt & Advanced / 工程进阶

> 精通 Prompt 工程和复杂自动化模式。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 4.1 | Prompt engineering | [EN](guide/en/09-prompt-engineering.md) / [中文](guide/zh/09-prompt-engineering.md) | XML 标签、Few-shot、系统提示 |
| 4.2 | Advanced workflows | [EN](guide/en/10-advanced-workflows.md) / [中文](guide/zh/10-advanced-workflows.md) | 自动审查、测试生成、发布管理 |

**检查点**: Prompt 能持续产出优秀结果，已搭建自动化审查和测试工作流。

---

### Stage 5: Production / 生产与运维

> 自信地将 AI 辅助代码交付到生产环境。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 5.1 | End-to-end project | [EN](guide/en/11-end-to-end-project.md) / [中文](guide/zh/11-end-to-end-project.md) | 从想法到部署的完整项目 |
| 5.2 | CI/CD integration | [EN](guide/en/12-cicd-integration.md) / [中文](guide/zh/12-cicd-integration.md) | AI 审查 PR、生成测试 |
| 5.3 | Cost & model selection | [EN](guide/en/13-cost-and-model-selection.md) / [中文](guide/zh/13-cost-and-model-selection.md) | Opus/Sonnet/Haiku、Token 省钱 |
| 5.4 | Debugging AI code | [EN](guide/en/14-debugging-ai-code.md) / [中文](guide/zh/14-debugging-ai-code.md) | 幻觉、回滚、预防模式 |

**检查点**: 能端到端交付完整项目、运行 AI 驱动的 CI/CD、有效控制成本。

---

### Stage 6: Team & Enterprise / 团队与企业

> 在团队中规模化推广 AI 辅助开发，确保安全合规。

| Step | Topic | Guide | 说明 |
|------|-------|-------|------|
| 6.1 | Team workflows | [EN](guide/en/15-team-workflows.md) / [中文](guide/zh/15-team-workflows.md) | 多人+AI 协作、PR 流程 |
| 6.2 | Security & compliance | [EN](guide/en/16-security-compliance.md) / [中文](guide/zh/16-security-compliance.md) | Secrets、OWASP、审计 |
| 6.3 | Large codebase | [EN](guide/en/17-large-codebase.md) / [中文](guide/zh/17-large-codebase.md) | 10万行代码的上下文策略 |

**检查点**: 团队高效地与 AI 协作、通过安全审计、管理大型代码库。

---

## 按角色快速定位 / Quick Reference by Role

| 角色 / Role | 从这里开始 | 重点 |
|-------------|-----------|------|
| 初学者 / Beginner | Stage 1 | 先跑起来，用 /init 生成 CLAUDE.md |
| 开发者 / Developer | Stage 2 | CLI 精通、Hooks、MCP |
| API 开发者 / API Builder | Stage 3 | Claude API、Agent SDK |
| 高级用户 / Power User | Stage 4 | Prompt 工程、高级自动化 |
| 上线交付 / Shipping to Prod | Stage 5 | 端到端实战、CI/CD、成本控制 |
| 技术负责人 / Tech Lead | Stage 6 | 团队协作、安全合规、大项目管理 |

---

## 按主题查找 / Browse by Topic

不按阶段，按"我想解决什么问题"查找：

| 层次 | 主题 | 章节 | 核心问题 |
|------|------|------|---------|
| 认知 | Human-AI 协作 | [01](guide/zh/01-getting-started.md) | AI 能帮我做什么？边界在哪？ |
| 认知 | Context Engineering | [03](guide/zh/03-claude-md-guide.md) | 怎么设计上下文让 AI 表现最好？ |
| 认知 | AI 代码质量思维 | [14](guide/zh/14-debugging-ai-code.md) | 怎么预防 AI 写出问题代码？ |
| 工具 | Claude Code CLI | [02](guide/zh/02-claude-code-mastery.md) | 怎么高效使用 CLI？ |
| 工具 | Hooks & MCP | [04](guide/zh/04-hooks-and-automation.md) · [05](guide/zh/05-mcp-servers.md) | 怎么自动化和扩展？ |
| 工具 | 多 Agent 编排 | [06](guide/zh/06-multi-agent.md) | 怎么协调多个 Agent？ |
| 工具 | API / Agent SDK | [07](guide/zh/07-api-and-sdk.md) · [08](guide/zh/08-agent-sdk.md) | 怎么用代码调用和构建 Agent？ |
| 工程 | Prompt 工程 | [09](guide/zh/09-prompt-engineering.md) | 怎么写出好 Prompt？ |
| 工程 | 成本控制 | [13](guide/zh/13-cost-and-model-selection.md) | 怎么省钱？选哪个模型？ |
| 工程 | 安全合规 | [16](guide/zh/16-security-compliance.md) | 怎么保证 AI 代码安全？ |
| 工程 | 大型代码库 | [17](guide/zh/17-large-codebase.md) | 10 万行代码怎么用 AI？ |
| 落地 | 端到端项目 | [11](guide/zh/11-end-to-end-project.md) | 从想法到部署的全流程？ |
| 落地 | CI/CD 集成 | [12](guide/zh/12-cicd-integration.md) | 怎么集成到流水线？ |
| 落地 | 团队协作 | [15](guide/zh/15-team-workflows.md) | 团队怎么一起用 AI？ |
| 落地 | 工作流框架 | [框架对比](examples/frameworks/) | 10 个框架该选哪个？ |

---

## 速查资源 / Resources

| 资源 | 链接 | 说明 |
|------|------|------|
| 中文速查表 | [cheatsheet_zh.md](cheatsheet_zh.md) | 命令/快捷键/API 速查 |
| English Cheatsheet | [cheatsheet.md](cheatsheet.md) | Commands/shortcuts/API |
| 工具对比 | [comparison.md](comparison.md) | Claude Code vs Cursor vs Copilot vs Windsurf |
| 项目模板 | [templates/](templates/) | CLAUDE.md 模板（6 种语言 + 全栈） |
| 代码示例 | [examples/](examples/) | 可运行代码 + 10 个工作流框架 |
| 资源集合 | [awesome.md](awesome.md) | 精选工具、库、文章 |

---

<p align="center">
  <sub>Part of <a href="README.md">claude-engineer</a> — give it a star to bookmark your learning journey!</sub>
</p>
