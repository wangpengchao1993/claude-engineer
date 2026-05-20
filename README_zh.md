<p align="center">
  <img src="assets/banner.png" alt="Claude Engineer Banner" width="800">
</p>

<h1 align="center">Claude Engineer</h1>

<p align="center">
  <strong>全面掌握 Claude 的终极指南 — 从 Claude Code CLI 到 API 到 Agent SDK。</strong>
</p>

<p align="center">
  <a href="https://github.com/anthropics/claude-code"><img src="https://img.shields.io/badge/Claude%20Code-Latest-blueviolet?logo=anthropic" alt="Claude Code"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/English-README-blue" alt="English"></a>
</p>

---

## 为什么选择这个仓库？

- **一站式参考** — 涵盖 Claude Code CLI、API、Agent SDK、MCP、Prompt 工程等所有内容。
- **即拿即用** — 提供 `CLAUDE.md`、Hooks、系统 Prompt、MCP 配置等模板，复制即可使用。
- **真实案例** — 可运行的代码示例，覆盖 Agent、Tool Use、流式处理和自动化工作流。

### 快速导航

| 我想... | 去这里 |
|---------|-------|
| 从零开始学 | [指南 01](guide/zh/01-getting-started.md) |
| 用 AI 做一个完整项目 | [指南 11 — 端到端实战](guide/zh/11-end-to-end-project.md) |
| 选一个工作流框架 | [框架对比](examples/frameworks/) |
| 抄一个 CLAUDE.md 模板 | [模板目录](templates/) — Python · C++ · Java · TS · Rust · 全栈 |
| 搭 AI CI/CD 流水线 | [CI/CD 模板](examples/cicd-templates/) |
| 省 Token 钱 | [指南 13 — 成本与模型选择](guide/zh/13-cost-and-model-selection.md) |

---

## 学习路线图

> 从入门到专家的完整路径。完整路线图：[roadmap.md](roadmap.md)

```
🟢 阶段 1：入门                 🔵 阶段 2：日常使用
   安装 → 首次对话 →               交互模式 → Plan 模式 →
   创建 CLAUDE.md                  Git 工作流 → 上下文管理

🟡 阶段 3：高级用户             🔴 阶段 4：专家
   Hooks → MCP 服务器 →           Claude API → Agent SDK →
   Prompt 工程                     多 Agent → CI/CD 集成
```

---

## 快速导航

| 板块 | 说明 |
|------|------|
| [学习路线图](roadmap.md) | 从入门到专家的分阶段学习路径 |
| [速查表](cheatsheet.md) | 命令、快捷键和技巧速查 |
| [教程指南](guide/zh/) | 从入门到高级的深度教程 |
| [模板](templates/) | 即用型 CLAUDE.md、Hook 和 Prompt 模板 |
| [代码示例](examples/) | 可运行的代码示例 |
| [资源列表](awesome.md) | 精选工具、MCP Server、文章等资源 |

---

## 速查表精选

> 完整速查表：[cheatsheet.md](cheatsheet.md)

### Claude Code 核心命令

| 命令 | 说明 |
|------|------|
| `claude` | 启动交互式 REPL |
| `claude "问题"` | 一次性查询，不进入交互模式 |
| `cat file \| claude "解释"` | 管道输入内容进行分析 |
| `claude -c` | 恢复最近的对话 |
| `claude --model` | 指定使用的模型 |
| `/init` | 为项目生成 CLAUDE.md 文件 |
| `/compact` | 压缩对话上下文 |
| `/mcp` | 管理 MCP 服务器 |
| `/cost` | 显示 Token 使用量和费用 |
| Shift+Tab | 切换 Plan 模式（先思考再行动） |
| Esc (按两次) | 中断 Claude 生成 |

### CLAUDE.md 快速示例

```markdown
# CLAUDE.md — 放在项目根目录

## 项目概述
简要描述项目功能。

## 技术栈
- 语言：TypeScript
- 框架：Next.js 14
- 数据库：PostgreSQL + Prisma

## 常用命令
- `npm run dev` — 启动开发服务器
- `npm test` — 运行测试
- `npm run lint` — 运行代码检查

## 代码规范
- 使用函数式组件 + Hooks
- 优先使用命名导出
- 错误信息应对用户友好
```

---

## 教程指南 — 目录

### 入门
- [01 - Claude 入门](guide/zh/01-getting-started.md) — 安装、配置和你的第一次对话

### Claude Code 精通
- [02 - Claude Code 精通](guide/zh/02-claude-code-mastery.md) — 深入 Claude Code CLI 的功能和工作流
- [03 - CLAUDE.md 指南](guide/zh/03-claude-md-guide.md) — 项目级配置的最佳实践
- [04 - Hooks 与自动化](guide/zh/04-hooks-and-automation.md) — 使用 Hooks 和 Shell 集成自动化工作流
- [05 - MCP 服务器](guide/zh/05-mcp-servers.md) — 通过 Model Context Protocol 扩展 Claude 的能力
- [06 - 多 Agent 模式](guide/zh/06-multi-agent.md) — 编排多个 Claude Agent 完成复杂任务

### API 与 SDK
- [07 - API 与 SDK](guide/zh/07-api-and-sdk.md) — 使用 Claude API 和 Anthropic SDK 构建应用
- [08 - Agent SDK](guide/zh/08-agent-sdk.md) — 使用 Claude Agent SDK 构建自定义 Agent

### Prompt 工程
- [09 - Prompt 工程](guide/zh/09-prompt-engineering.md) — 从 Claude 获得最佳结果的技巧
- [10 - 高级工作流](guide/zh/10-advanced-workflows.md) — 复杂的实际自动化模式

### 生产与运维 🆕
- [11 - 端到端实战](guide/zh/11-end-to-end-project.md) — 用 AI 从想法到部署完成一个完整应用
- [12 - CI/CD 集成](guide/zh/12-cicd-integration.md) — AI 驱动的代码审查、测试和部署流水线
- [13 - 成本与模型选择](guide/zh/13-cost-and-model-selection.md) — Opus vs Sonnet vs Haiku、Token 预算、省钱策略
- [14 - 调试 AI 代码](guide/zh/14-debugging-ai-code.md) — AI 出错时：发现、恢复、预防

### 团队与企业 🆕
- [15 - 团队协作](guide/zh/15-team-workflows.md) — 多人 + AI 协作、PR 流程、新人入职
- [16 - 安全合规](guide/zh/16-security-compliance.md) — Secrets 管理、OWASP、审计日志、合规
- [17 - 大项目管理](guide/zh/17-large-codebase.md) — 10 万行代码的上下文策略、单仓库模式

---

## 模板

即用模板 — 直接复制到你的项目中：

| 模板 | 说明 |
|------|------|
| [CLAUDE.md](templates/CLAUDE.md) | 通用项目配置模板 |
| [CLAUDE-python.md](templates/CLAUDE-python.md) | Python 项目模板 |
| [CLAUDE-typescript.md](templates/CLAUDE-typescript.md) | TypeScript/Node.js 项目模板 |
| [CLAUDE-rust.md](templates/CLAUDE-rust.md) | Rust 项目模板 |
| [CLAUDE-cpp.md](templates/CLAUDE-cpp.md) | C++ 项目模板（CMake, GTest, clang-tidy）🆕 |
| [CLAUDE-java.md](templates/CLAUDE-java.md) | Java 项目模板（Spring Boot, Maven, JUnit 5）🆕 |
| [CLAUDE-fullstack.md](templates/CLAUDE-fullstack.md) | 全栈项目模板（前端+后端+数据库）🆕 |
| [系统 Prompt](templates/system-prompts/) | 代码审查、写作、分析等场景的 Prompt |
| [Hook 脚本](templates/hooks/) | 预提交检查、自动测试等 |
| [安全模板](templates/security/) | 安全钩子、AI 代码 OWASP 检查清单 🆕 |

---

## 代码示例

按类别组织的可运行代码示例：

### 全栈示例 🆕
- [任务管理器 Demo](examples/fullstack-demo/) — 完整项目：CLAUDE.md + 钩子 + CI/CD + Docker

### CI/CD 模板 🆕
- [AI 代码审查](examples/cicd-templates/github-actions/ai-code-review.yml) — GitHub Actions：AI 审查每个 PR
- [AI 测试生成](examples/cicd-templates/github-actions/ai-test-gen.yml) — 自动为改动文件生成测试
- [GitLab CI](examples/cicd-templates/gitlab-ci/) — GitLab 等效流水线

### Claude Code
- [Hook 配置](examples/claude-code/hooks/) — 自定义自动化 Hook
- [MCP 服务器配置](examples/claude-code/mcp-configs/) — 即用型 MCP 配置
- [CLAUDE.md 示例](examples/claude-code/claude-md/) — 真实项目配置

### API 与 SDK
- [Tool Use 模式](examples/api/tool-use/) — 函数调用与工具集成
- [流式处理](examples/api/streaming/) — 实时流式响应
- [多模态](examples/api/multimodal/) — 图像和 PDF 处理

### Agent
- [简单 Agent](examples/agents/simple-agent/) — 带工具的基础 Agent
- [多 Agent](examples/agents/multi-agent/) — Agent 编排模式
- [代码审查 Bot](examples/agents/code-review-bot/) — 实用的自动化代码审查工具

### AI 编码工作流框架 🆕

> 将 AI 编码变成结构化工程流程的 Harness 框架：需求→设计→实现→审查→交付。

| 分类 | 框架 |
|------|------|
| 方法论 | [Superpowers](examples/frameworks/superpowers/) · [GSD](examples/frameworks/gsd/) · [Spec-Kit](examples/frameworks/spec-kit/) · [BMAD](examples/frameworks/bmad-method/) |
| 虚拟团队 | [GStack](examples/frameworks/gstack/) · [ECC](examples/frameworks/ecc/) |
| 编排进化 | [Hermes Agent](examples/frameworks/hermes-agent/) · [Citadel](examples/frameworks/citadel/) |
| 全生命周期 | [CC Harness](examples/frameworks/claude-code-harness/) · [CC Workflows](examples/frameworks/claude-code-workflows/) |

👉 **[完整指南与对比 →](examples/frameworks/)**

---

## 资源列表

> 完整列表：[awesome.md](awesome.md)

### 官方资源
- [Claude Code](https://github.com/anthropics/claude-code) — Anthropic 官方 CLI 工具
- [Anthropic SDK (Python)](https://github.com/anthropics/anthropic-sdk-python) — 官方 Python SDK
- [Anthropic SDK (TypeScript)](https://github.com/anthropics/anthropic-sdk-typescript) — 官方 TypeScript SDK
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk) — 构建自定义 Agent
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — 官方代码示例

---

## 参与贡献

欢迎贡献！无论是修复错别字、添加新模板还是编写指南，每一份贡献都有价值。

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

---

## 许可证

本项目基于 [MIT 许可证](LICENSE) 发布。

---

<p align="center">
  <sub>如果你觉得有用，请给个 Star！这有助于更多人发现这个资源。</sub>
</p>
