# Spec-Kit -- GitHub's Official Spec-Driven Development

# Spec-Kit -- GitHub 官方规格驱动开发框架

> By GitHub | Open Source | Claude Code Plugin
>
> 由 GitHub 开发 | 开源 | Claude Code 插件

---

## What is Spec-Kit? / 什么是 Spec-Kit?

Instead of telling AI "build me an app" and hoping for the best, Spec-Kit makes you
define principles, requirements, and plans **before** any code is written. Think of it
as **an architect who won't let you build without blueprints**.

与其对 AI 说"帮我做个应用"然后听天由命, Spec-Kit 要求你在写任何代码之前先定义原则、
需求和计划。可以把它想象成 **一个不让你没有蓝图就动工的建筑师**。

Traditional AI coding / 传统 AI 编程:

```
"Build me a todo app" --> (AI guesses everything) --> Messy result
"帮我做个待办应用"     --> (AI 自行猜测一切)        --> 混乱的结果
```

Spec-Kit approach / Spec-Kit 方式:

```
Constitution --> Specify --> Clarify --> Plan --> Tasks --> Implement
宪法(原则)  --> 规格说明 --> 澄清歧义 --> 规划  --> 任务拆分 --> 执行实现
```

---

## Core Workflow: 6 Phases / 核心工作流: 6 个阶段

```
Phase 1: Constitution  -- Define non-negotiable rules (technologies, style, constraints)
阶段 1: 宪法(原则)     -- 定义不可违背的规则（技术栈、风格、约束条件）

Phase 2: Specify       -- Outline requirements and features
阶段 2: 规格说明        -- 概述需求和功能

Phase 3: Clarify       -- Resolve ambiguities and open questions
阶段 3: 澄清歧义        -- 解决模糊点和开放性问题

Phase 4: Plan          -- Create a detailed implementation plan
阶段 4: 规划            -- 创建详细的实施计划

Phase 5: Tasks         -- Break the plan into concrete work items
阶段 5: 任务拆分        -- 将计划拆分为具体的工作项

Phase 6: Implement     -- Execute each task following the constitution
阶段 6: 执行实现        -- 按照宪法原则执行每个任务
```

Each phase feeds into the next. You cannot skip ahead -- the framework enforces
discipline so AI-generated code stays aligned with your intent.

每个阶段的输出作为下一阶段的输入。你不能跳过任何阶段 -- 框架强制执行纪律,
确保 AI 生成的代码始终与你的意图一致。

---

## 9 Slash Commands / 9 个斜杠命令

| Command / 命令 | Purpose / 用途 | Phase / 阶段 |
|---|---|---|
| `/speckit.constitution` | Define project principles and constraints / 定义项目原则和约束 | 1 - Constitution |
| `/speckit.specify` | Create requirements specification / 创建需求规格说明 | 2 - Specify |
| `/speckit.clarify` | Resolve ambiguities in the spec / 解决规格中的歧义 | 3 - Clarify |
| `/speckit.plan` | Generate implementation plan / 生成实施计划 | 4 - Plan |
| `/speckit.tasks` | Break plan into task list / 将计划拆分为任务列表 | 5 - Tasks |
| `/speckit.implement` | Execute tasks one by one / 逐一执行任务 | 6 - Implement |
| `/speckit.analyze` | Analyze existing code against spec / 根据规格分析现有代码 | Utility / 工具 |
| `/speckit.checklist` | Generate a compliance checklist / 生成合规检查清单 | Utility / 工具 |
| `/speckit.taskstoissues` | Export tasks as GitHub Issues / 将任务导出为 GitHub Issues | Utility / 工具 |

---

## What Goes in a Constitution? / 宪法中包含什么?

A Constitution is the foundation of every Spec-Kit project. It defines the
non-negotiable rules that all generated code must follow.

宪法是每个 Spec-Kit 项目的基础。它定义了所有生成代码必须遵守的不可违背的规则。

```yaml
# Example Constitution / 示例宪法
technologies:
  language: Python 3.12
  framework: FastAPI
  database: PostgreSQL

testing:
  required: true
  minimum_coverage: 80%
  framework: pytest

style:
  formatter: black
  linter: ruff
  max_line_length: 100

constraints:
  - No ORM magic -- use raw SQL with parameterized queries
    不使用 ORM 魔法 -- 使用带参数化查询的原始 SQL
  - All endpoints must have OpenAPI documentation
    所有端点必须有 OpenAPI 文档
  - Every function must have type hints
    每个函数必须有类型提示
```

---

## Installation / 安装

Spec-Kit is a Claude Code plugin. Install it from the plugin marketplace:

Spec-Kit 是 Claude Code 插件。从插件市场安装:

```bash
/plugin marketplace add github/spec-kit
```

That's it. The 9 slash commands become available immediately.

就这样。9 个斜杠命令立即可用。

---

## Extensions / 扩展

Spec-Kit supports domain-specific workflows and external tool integration:

Spec-Kit 支持领域特定工作流和外部工具集成:

- **Domain workflows / 领域工作流**: Customize constitution templates for web apps,
  CLI tools, data pipelines, mobile apps, etc.
  为 Web 应用、CLI 工具、数据管道、移动应用等定制宪法模板。

- **External tools / 外部工具**: Integrate with GitHub Issues (`/speckit.taskstoissues`),
  project boards, CI/CD pipelines, and more.
  与 GitHub Issues (`/speckit.taskstoissues`)、项目看板、CI/CD 管道等集成。

- **Custom rules / 自定义规则**: Add organization-specific constraints to the
  constitution (security policies, accessibility standards, etc.).
  在宪法中添加组织特定的约束（安全策略、无障碍标准等）。

---

## Spec-Kit vs BMAD-METHOD / Spec-Kit 与 BMAD-METHOD 对比

| Aspect / 方面 | Spec-Kit | BMAD-METHOD |
|---|---|---|
| Creator / 创建者 | GitHub (official) / GitHub（官方） | Community / 社区 |
| Approach / 方法 | Spec-driven, document-first / 规格驱动, 文档优先 | Agile, role-based personas / 敏捷, 基于角色的人格 |
| Structure / 结构 | Linear phases (Constitution to Implement) / 线性阶段 | Flexible agent roles (PM, Architect, Dev) / 灵活的代理角色 |
| Best for / 最适合 | Projects needing strict compliance / 需要严格合规的项目 | Fast iteration and prototyping / 快速迭代和原型开发 |
| Philosophy / 理念 | "Define everything before building" / "构建前定义一切" | "Collaborate like a real team" / "像真实团队一样协作" |

Both are valid approaches. Spec-Kit excels when you need auditability and
consistency. BMAD-METHOD excels when you need speed and flexibility.

两者都是有效的方法。当你需要可审计性和一致性时, Spec-Kit 更出色。
当你需要速度和灵活性时, BMAD-METHOD 更出色。

---

## Learn More / 了解更多

- Repository / 仓库: [github.com/github/spec-kit](https://github.com/github/spec-kit)
- Documentation / 文档: See the repo's docs folder for detailed guides
  查看仓库的 docs 文件夹获取详细指南

---

*Spec-Kit enforces the discipline that turns AI from a guessing machine into a
precision tool. Define first, build second.*

*Spec-Kit 强制执行纪律, 将 AI 从猜测机器变成精密工具。先定义, 再构建。*
