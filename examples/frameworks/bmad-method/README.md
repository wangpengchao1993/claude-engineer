# BMAD-METHOD -- Agile AI-Driven Development / 敏捷 AI 驱动开发方法

> By [bmad-code-org](https://github.com/bmad-code-org/BMAD-METHOD) | MIT License

## What is BMAD-METHOD? / 什么是 BMAD-METHOD？

**BMAD** stands for **Breakthrough Method for Agile AI-Driven Development**.
It is a multi-agent framework that creates a virtual agile team where each AI agent
plays a specific role -- Product Manager, Architect, Developer, QA Engineer, and DevOps.

Think of it as **running a full agile sprint with AI teammates**.
You bring the idea; the agents handle requirements, design, code, testing, and deployment.

**BMAD** 全称 **Breakthrough Method for Agile AI-Driven Development**（突破性敏捷 AI 驱动开发方法）。
它是一个多智能体框架，创建一个虚拟敏捷团队，每个 AI 智能体扮演特定角色——
产品经理、架构师、开发者、QA 工程师和 DevOps 工程师。

你可以把它理解为**让 AI 队友帮你跑一个完整的敏捷冲刺**。
你只需提出想法，智能体们负责需求、设计、编码、测试和部署。

---

## Agent Roles / 智能体角色

| Role / 角色 | Responsibility / 职责 | Output / 产出 |
|---|---|---|
| **Product Manager / 产品经理** | Gather requirements, write user stories / 收集需求，编写用户故事 | PRD, user stories / 产品需求文档、用户故事 |
| **Architect / 架构师** | Design system architecture, choose tech stack / 设计系统架构，选择技术栈 | Architecture doc, tech stack / 架构文档、技术栈 |
| **Developer / 开发者** | Implement features based on the design / 根据设计实现功能 | Working code / 可运行的代码 |
| **QA Engineer / QA 工程师** | Write and run tests, verify quality / 编写和运行测试，验证质量 | Test suite, bug reports / 测试套件、缺陷报告 |
| **DevOps / DevOps 工程师** | Configure CI/CD, deploy to production / 配置 CI/CD，部署到生产环境 | Deployment pipeline / 部署流水线 |

---

## Workflow / 工作流程

The BMAD workflow follows a natural agile sprint cycle:

BMAD 的工作流程遵循自然的敏捷冲刺周期：

```
Idea / 想法
  |
  v
Product Manager -- defines requirements & user stories
产品经理 -- 定义需求和用户故事
  |
  v
Architect -- designs system architecture & tech stack
架构师 -- 设计系统架构和技术栈
  |
  v
Developer -- implements features based on architecture
开发者 -- 根据架构实现功能
  |
  v
QA Engineer -- writes tests, verifies quality
QA 工程师 -- 编写测试，验证质量
  |
  v
DevOps -- deploys to production
DevOps 工程师 -- 部署到生产环境
  |
  v
Working Software / 可运行的软件
```

Each phase feeds into the next. The team can iterate -- just like a real agile sprint.

每个阶段的产出作为下一个阶段的输入。团队可以迭代——就像真正的敏捷冲刺一样。

---

## Installation / 安装

### Option 1: NPX (official CLI) / 方式一：NPX（官方命令行）

```bash
npx bmad-method@next install
```

This scaffolds the BMAD project structure and agent configurations in your repo.

这会在你的仓库中创建 BMAD 项目结构和智能体配置文件。

### Option 2: Claude Code Native Skills / 方式二：Claude Code 原生技能

BMAD can also run as Claude Code skills -- each agent becomes a slash command
you invoke inside Claude Code.

BMAD 也可以作为 Claude Code 技能运行——每个智能体成为你在 Claude Code 中调用的斜杠命令。

---

## Key Features / 核心特性

- **Domain-specific modules / 领域模块**: Tailored agent behaviors for web apps, APIs,
  data pipelines, and more. 针对 Web 应用、API、数据管道等场景定制智能体行为。

- **Codebase Flattener tool / 代码库扁平化工具**: Aggregates your entire codebase into a
  single XML file optimized for AI consumption. Useful for giving an agent full project
  context in one shot. 将整个代码库聚合为一个 XML 文件，便于 AI 一次性获取完整项目上下文。

- **Iterative sprints / 迭代冲刺**: Agents loop through build-test-fix cycles automatically.
  智能体自动循环执行构建-测试-修复流程。

- **Customizable roles / 可自定义角色**: Add, remove, or modify agent roles to fit your team's
  workflow. 可增删或修改智能体角色以适应你的团队流程。

---

## Available Implementations / 可用实现

| Implementation / 实现 | Description / 说明 |
|---|---|
| [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) (official) | The original multi-agent framework / 官方多智能体框架 |
| [Claude Code Native Skills](https://github.com/aj-geddes) (aj-geddes) | BMAD agents as Claude Code slash commands / BMAD 智能体作为 Claude Code 斜杠命令 |
| [BMAD Plugin](https://github.com/PabloLION) (PabloLION) | Plugin-based integration for existing projects / 基于插件的集成方案 |

---

## BMAD vs Spec-Kit / BMAD 与 Spec-Kit 的对比

| Aspect / 方面 | BMAD-METHOD | Spec-Kit |
|---|---|---|
| **Philosophy / 理念** | Agile, iterative / 敏捷、迭代 | Waterfall, structured / 瀑布式、结构化 |
| **Approach / 方式** | Agents collaborate in sprints / 智能体在冲刺中协作 | Linear document-driven flow / 线性文档驱动流程 |
| **Flexibility / 灵活性** | High -- agents adapt mid-sprint / 高——智能体可在冲刺中调整 | Moderate -- follows a fixed plan / 中等——遵循固定计划 |
| **Best for / 适用于** | Evolving requirements, rapid prototyping / 需求多变、快速原型 | Well-defined specs, compliance-heavy projects / 需求明确、合规要求高的项目 |

---

## Learn More / 了解更多

- GitHub: [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- Try the example: see `example_workflow.py` in this directory
- Run the tests: `pytest test_bmad.py -v`

---

*This example is part of the Claude Engineer frameworks collection.*

*本示例是 Claude Engineer 框架合集的一部分。*
