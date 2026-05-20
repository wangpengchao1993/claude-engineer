# Claude Code Workflows -- Full-Lifecycle Development / 全生命周期开发工作流

**By [shinpr](https://github.com/shinpr/claude-code-workflows) | Open Source**

## What Is It? / 这是什么?

Claude Code Workflows is a framework of production-ready development workflows for Claude Code.
It automates the entire software development lifecycle -- from an initial idea all the way to
verified, tested code. Specialized agents handle requirements analysis, design, implementation,
and quality checks so that you ship code that actually matches its design documents and passes
its tests.

Claude Code Workflows 是一套面向 Claude Code 的生产级开发工作流框架。
它将软件开发的完整生命周期自动化 -- 从最初的想法到经过验证和测试的代码。
专用智能体分别负责需求分析、设计、实现和质量检查，确保交付的代码真正符合设计文档并通过所有测试。

Think of it as: **a complete software development lifecycle, automated**.
可以把它理解为：**一条完全自动化的软件开发流水线**。

---

## Full Lifecycle / 完整生命周期

The framework walks every feature through a structured pipeline:

框架让每个功能特性都经过一套结构化流水线：

```
Idea / 想法
  -> Complexity Analysis / 复杂度分析
    -> PRD (Product Requirements Document / 产品需求文档)
      -> UI Spec / UI 规格说明
        -> Design Doc / 设计文档
          -> Work Plan / 工作计划
            -> Implementation / 实现
              -> Tests / 测试
                -> Verification / 验证
```

Each stage produces a concrete artifact that feeds into the next stage.
每个阶段都产出具体的制品，供下一阶段使用。

---

## Core Components / 核心组件

### Requirement Analyzer / 需求分析器

Automatically detects task complexity (small, medium, large) and picks the
appropriate workflow. A small bug fix skips straight to implementation; a large
feature goes through the full pipeline.

自动检测任务复杂度（小型、中型、大型），并选择合适的工作流。
小型 bug 修复直接进入实现阶段；大型功能特性则走完整流水线。

### Codebase Analyzer / 代码库分析器

Before any design work begins, the analyzer scans your codebase -- modules,
dependencies, authentication flows, API boundaries -- so that generated
documents reflect your actual architecture.

在任何设计工作开始之前，分析器会扫描你的代码库 -- 模块、依赖、认证流程、API 边界 --
确保生成的文档反映真实的架构。

### Generated Artifacts / 生成的制品

| Artifact / 制品 | Purpose / 用途 |
|---|---|
| **PRD** | Product requirements: goals, user stories, acceptance criteria / 产品需求：目标、用户故事、验收标准 |
| **UI Spec** | Screen layouts, component hierarchy, interaction flows / 界面布局、组件层级、交互流程 |
| **Design Doc** | Architecture decisions, data models, API contracts / 架构决策、数据模型、API 契约 |
| **Work Plan** | Ordered implementation tasks with dependencies / 有序的实现任务及其依赖关系 |

### Specialized Agents / 专用智能体

- **Requirement Agent / 需求智能体** -- analyzes the idea, determines scope and complexity / 分析想法，确定范围和复杂度
- **Design Agent / 设计智能体** -- produces PRD, UI Spec, and Design Doc / 生成 PRD、UI 规格说明和设计文档
- **Implementation Agent / 实现智能体** -- writes code following the work plan / 按照工作计划编写代码
- **Quality Agent / 质量智能体** -- runs tests, verifies that code matches the design doc / 运行测试，验证代码是否符合设计文档

---

## Plugins / 插件

### Discover

Turns raw feature ideas into polished PRDs. Great for brainstorming sessions
where you have many ideas and want structured documents for each.

将原始的功能想法转化为完善的 PRD。非常适合头脑风暴场景 -- 把大量想法逐一转化为结构化文档。

### Metronome

A guardrail plugin that prevents shortcut-taking during implementation. It
checks that each implementation step still aligns with the design doc and
flags any drift.

一个防护插件，防止在实现过程中偷工减料。它检查每个实现步骤是否仍然与设计文档一致，并标记任何偏差。

### Linear-Prism

Converts requirements into Linear tasks automatically. If your team uses
Linear for project management, this plugin bridges the gap between
Workflows and your task board.

自动将需求转换为 Linear 任务。如果你的团队使用 Linear 做项目管理，
这个插件可以在 Workflows 和你的任务看板之间搭建桥梁。

---

## Installation / 安装

```bash
/plugin marketplace add shinpr/claude-code-workflows
```

After installation the workflow commands are available in your Claude Code session.
安装后，工作流命令即可在你的 Claude Code 会话中使用。

---

## Key Differentiator / 核心差异

Most coding assistants generate code and stop there. Claude Code Workflows
generates **full documentation first** -- PRD, UI Spec, Design Doc, Work Plan --
and only then writes code that is verified against those documents. This means
fewer surprises, fewer rewrites, and a clear paper trail for every decision.

大多数编码助手只生成代码就结束了。Claude Code Workflows 会**先生成完整文档** --
PRD、UI 规格说明、设计文档、工作计划 -- 然后才编写代码，并对照这些文档进行验证。
这意味着更少的意外、更少的返工，以及每个决策的清晰记录。

### Comparison with Spec-Kit / 与 Spec-Kit 的比较

| | Workflows | Spec-Kit |
|---|---|---|
| Approach / 方式 | Automated pipeline / 自动化流水线 | Manual / interactive / 手动交互式 |
| Artifacts / 制品 | Auto-generated PRD, Design Doc, etc. / 自动生成 | User-authored specs / 用户手写规格 |
| Best for / 最适合 | Teams wanting end-to-end automation / 需要端到端自动化的团队 | Teams wanting fine-grained control / 需要精细控制的团队 |

---

## Learn More / 了解更多

- GitHub: [github.com/shinpr/claude-code-workflows](https://github.com/shinpr/claude-code-workflows)
