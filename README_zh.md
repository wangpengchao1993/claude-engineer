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

---

## 从哪里开始？

| 我想... | 去这里 |
|---------|-------|
| 先看全貌，了解整体知识结构 | [知识体系总览](overview.md) |
| 按路线从零开始学 | [学习路线图](roadmap.md) → [第 01 章：入门](guide/zh/01-getting-started.md) |
| 查一个命令 / 快捷键 / API 参数 | [中文速查表](cheatsheet_zh.md) |
| 了解 Claude Code 和其他工具的区别 | [AI 工具对比](comparison.md) |
| 直接抄一个项目模板 | [模板目录](templates/) — Python · C++ · Java · TS · Rust · 全栈 |
| 用 AI 做一个完整项目 | [第 11 章：端到端实战](guide/zh/11-end-to-end-project.md) |
| 搭 AI CI/CD 流水线 | [第 12 章：CI/CD 集成](guide/zh/12-cicd-integration.md) |
| 省 Token 钱 | [第 13 章：成本与模型选择](guide/zh/13-cost-and-model-selection.md) |
| 找工具、库、文章等资源 | [资源列表](awesome.md) |

---

## 学习路线

> 完整路线图：[roadmap.md](roadmap.md)

```
阶段 1：入门                 阶段 2：日常使用
  安装 → 首次对话 →             交互模式 → Plan 模式 →
  创建 CLAUDE.md                Git 工作流 → 上下文管理

阶段 3：高级用户             阶段 4：专家
  Hooks → MCP 服务器 →         Claude API → Agent SDK →
  Prompt 工程                   多 Agent → CI/CD 集成
```

---

## 教程指南（17 章，中英双语）

按照从入门到深入的顺序排列，建议顺序阅读。

### 第一阶段：入门

| 章节 | 主题 | 你会学到 |
|------|------|---------|
| [01](guide/zh/01-getting-started.md) | Claude 入门 | 安装、配置、第一次对话 |

### 第二阶段：Claude Code 精通

| 章节 | 主题 | 你会学到 |
|------|------|---------|
| [02](guide/zh/02-claude-code-mastery.md) | CLI 精通 | 交互/非交互模式、管道、Plan 模式 |
| [03](guide/zh/03-claude-md-guide.md) | CLAUDE.md 指南 | 项目配置、上下文工程、多层级规则 |
| [04](guide/zh/04-hooks-and-automation.md) | Hooks 与自动化 | 事件钩子、自动 lint、质量守护 |
| [05](guide/zh/05-mcp-servers.md) | MCP 服务器 | 扩展 Claude 的工具能力 |
| [06](guide/zh/06-multi-agent.md) | 多 Agent 模式 | 子 Agent、并行执行、任务编排 |

### 第三阶段：API 与 SDK

| 章节 | 主题 | 你会学到 |
|------|------|---------|
| [07](guide/zh/07-api-and-sdk.md) | API 与 SDK | 用代码调用 Claude（Python/TypeScript） |
| [08](guide/zh/08-agent-sdk.md) | Agent SDK | 构建自定义 Agent |

### 第四阶段：Prompt 工程与高级模式

| 章节 | 主题 | 你会学到 |
|------|------|---------|
| [09](guide/zh/09-prompt-engineering.md) | Prompt 工程 | 结构化 Prompt、Claude 专属技巧 |
| [10](guide/zh/10-advanced-workflows.md) | 高级工作流 | 自动化审查、测试生成、发布管理 |

### 第五阶段：生产与运维

| 章节 | 主题 | 你会学到 |
|------|------|---------|
| [11](guide/zh/11-end-to-end-project.md) | 端到端实战 | 从想法到部署的完整 AI 开发流程 |
| [12](guide/zh/12-cicd-integration.md) | CI/CD 集成 | AI 驱动的代码审查和部署流水线 |
| [13](guide/zh/13-cost-and-model-selection.md) | 成本与模型选择 | Opus/Sonnet/Haiku 对比、省钱策略 |
| [14](guide/zh/14-debugging-ai-code.md) | 调试 AI 代码 | 常见 AI 错误、预防与修复 |

### 第六阶段：团队与企业

| 章节 | 主题 | 你会学到 |
|------|------|---------|
| [15](guide/zh/15-team-workflows.md) | 团队协作 | 多人 + AI 协作、PR 流程、新人入职 |
| [16](guide/zh/16-security-compliance.md) | 安全合规 | Secrets 管理、OWASP、审计、合规 |
| [17](guide/zh/17-large-codebase.md) | 大项目管理 | 10 万行代码的上下文策略、Monorepo |

---

## 模板

即用模板，复制到你的项目中：

| 模板 | 说明 |
|------|------|
| [CLAUDE.md](templates/CLAUDE.md) | 通用项目配置模板 |
| [CLAUDE-python.md](templates/CLAUDE-python.md) | Python 项目模板 |
| [CLAUDE-typescript.md](templates/CLAUDE-typescript.md) | TypeScript/Node.js 项目模板 |
| [CLAUDE-rust.md](templates/CLAUDE-rust.md) | Rust 项目模板 |
| [CLAUDE-cpp.md](templates/CLAUDE-cpp.md) | C++ 项目模板（CMake, GTest, clang-tidy） |
| [CLAUDE-java.md](templates/CLAUDE-java.md) | Java 项目模板（Spring Boot, Maven, JUnit 5） |
| [CLAUDE-fullstack.md](templates/CLAUDE-fullstack.md) | 全栈项目模板（前端+后端+数据库） |
| [系统 Prompt](templates/system-prompts/) | 代码审查、写作、分析等场景的 Prompt |
| [Hook 脚本](templates/hooks/) | 预提交检查、自动测试等 |
| [安全模板](templates/security/) | 安全钩子、AI 代码 OWASP 检查清单 |

---

## 代码示例

### 全栈示例
- [任务管理器 Demo](examples/fullstack-demo/) — 完整项目：CLAUDE.md + Hooks + CI/CD + Docker

### CI/CD 模板
- [AI 代码审查](examples/cicd-templates/github-actions/ai-code-review.yml) — GitHub Actions：AI 审查每个 PR
- [AI 测试生成](examples/cicd-templates/github-actions/ai-test-gen.yml) — 自动为改动文件生成测试
- [GitLab CI](examples/cicd-templates/gitlab-ci/) — GitLab 等效流水线

### Claude Code 配置
- [Hook 配置](examples/claude-code/hooks/) — 自定义自动化 Hook
- [MCP 服务器配置](examples/claude-code/mcp-configs/) — 即用型 MCP 配置
- [CLAUDE.md 示例](examples/claude-code/claude-md/) — 真实项目配置

### API 与 SDK
- [Tool Use 模式](examples/api/tool-use/) — 函数调用与工具集成
- [流式处理](examples/api/streaming/) — 实时流式响应

### Agent
- [简单 Agent](examples/agents/simple-agent/) — 带工具的基础 Agent
- [代码审查 Bot](examples/agents/code-review-bot/) — 自动化代码审查工具

### 工作流框架

> 将 AI 编码变成结构化工程流程：需求→设计→实现→审查→交付。

| 分类 | 框架 |
|------|------|
| 方法论 | [Superpowers](examples/frameworks/superpowers/) · [GSD](examples/frameworks/gsd/) · [Spec-Kit](examples/frameworks/spec-kit/) · [BMAD](examples/frameworks/bmad-method/) |
| 虚拟团队 | [GStack](examples/frameworks/gstack/) · [ECC](examples/frameworks/ecc/) |
| 编排 | [Hermes Agent](examples/frameworks/hermes-agent/) · [Citadel](examples/frameworks/citadel/) |
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
