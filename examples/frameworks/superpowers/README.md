# Superpowers -- The #1 Claude Code Skills Framework

# Superpowers -- 最受欢迎的 Claude Code 技能框架

> ~197k GitHub stars | By Jesse Vincent (obra) | MIT License
>
> GitHub: [github.com/obra/superpowers](https://github.com/obra/superpowers)

---

## What is Superpowers? / 什么是 Superpowers?

**English:**
Superpowers is an agentic skills framework that transforms Claude Code from a chatbot
into a disciplined senior developer. It refuses to write code until the design is
approved. Think of it as "hiring a senior engineer who insists on doing things right."

It works across Claude Code, Cursor, Codex, and other AI coding tools.

**中文:**
Superpowers 是一个智能技能框架，它把 Claude Code 从一个聊天机器人转变为一个有纪律的
高级开发者。在设计方案被批准之前，它会拒绝写代码。你可以把它想象成"雇了一个坚持正确
做事的高级工程师"。

它可以在 Claude Code、Cursor、Codex 等 AI 编程工具中使用。

---

## Core Workflow: 7 Phases / 核心工作流：7 个阶段

Superpowers enforces a structured software development methodology with 7 phases.
Each phase must complete before moving to the next.

Superpowers 强制执行一个结构化的软件开发方法论，包含 7 个阶段。
每个阶段必须完成后才能进入下一个。

```
Phase 1: Brainstorm    头脑风暴    Clarify requirements, ask questions, REFUSE to code
Phase 2: Write Spec    编写规格    Show spec in digestible chunks for approval
Phase 3: Write Plan    编写计划    Break work into 2-5 minute tasks
Phase 4: TDD           测试驱动    Red / Green / Refactor cycle
Phase 5: Subagent Dev  子代理开发  Fresh context per task (prevents context rot)
Phase 6: Review        代码审查    Check all work against spec
Phase 7: Finalize      最终确认    Clean up and deliver
```

### Why this order matters / 为什么顺序很重要

**English:**
- Phase 1 (Brainstorm) prevents building the wrong thing. Claude asks YOU questions
  instead of guessing.
- Phase 4 (TDD) ensures correctness: you write the test first, then the code.
- Phase 5 (Subagent) gives each task a fresh context window, preventing "context rot"
  where Claude forgets earlier instructions after long conversations.

**中文:**
- 阶段 1（头脑风暴）防止构建错误的东西。Claude 会向你提问，而不是猜测。
- 阶段 4（TDD）确保正确性：先写测试，再写代码。
- 阶段 5（子代理）为每个任务提供全新的上下文窗口，防止"上下文腐烂"——
  即长对话后 Claude 忘记了早期的指令。

---

## 14 Skills / 14 个技能

| # | Skill Name / 技能名称 | Purpose / 用途 |
|---|----------------------|----------------|
| 1 | brainstorming | Clarify requirements before coding / 编码前澄清需求 |
| 2 | writing-specs | Generate detailed specifications / 生成详细规格说明 |
| 3 | writing-plans | Break specs into small tasks / 将规格分解为小任务 |
| 4 | test-driven-development | Red-green-refactor cycle / 红-绿-重构循环 |
| 5 | subagent-driven-development | Dispatch tasks to fresh subagents / 将任务分派给新的子代理 |
| 6 | code-review | Review code against spec / 根据规格审查代码 |
| 7 | systematic-debugging | Structured approach to fixing bugs / 结构化的调试方法 |
| 8 | context-management | Keep context window clean / 保持上下文窗口整洁 |
| 9 | documentation | Generate docs from code / 从代码生成文档 |
| 10 | refactoring | Safe code restructuring / 安全的代码重构 |
| 11 | git-workflow | Conventional commits and branching / 规范化提交和分支管理 |
| 12 | dependency-management | Track and update dependencies / 追踪和更新依赖 |
| 13 | performance-optimization | Profile and optimize code / 分析和优化代码 |
| 14 | security-review | Check for vulnerabilities / 检查安全漏洞 |

---

## Installation / 安装

### Option 1: Plugin (Recommended / 推荐)

```bash
claude plugin add obra/superpowers
```

### Option 2: Manual Setup / 手动安装

Clone the repo and copy the skills into your project's `.claude/` directory:

将仓库克隆下来，把技能文件复制到你项目的 `.claude/` 目录中：

```bash
git clone https://github.com/obra/superpowers.git
cp -r superpowers/.claude/ your-project/.claude/
```

---

## Key Commands / 关键命令

| Command / 命令 | What it does / 功能 |
|----------------|---------------------|
| `/brainstorm` | Start requirements gathering / 开始需求收集 |
| `/spec` | Generate or review specification / 生成或审查规格说明 |
| `/plan` | Create implementation plan / 创建实施计划 |
| `/tdd` | Enter TDD mode (test first!) / 进入 TDD 模式（先写测试！） |
| `/review` | Review completed work / 审查完成的工作 |

### Example Session / 示例会话

```
You:    /brainstorm I need a URL shortener
Claude: Before I write any code, let me ask some questions:
        1. What's the expected traffic volume?
        2. Do you need custom short URLs?
        3. What database are you using?
        ...

You:    [answer questions]

Claude: /spec  -- Here's the specification...
Claude: /plan  -- Here are 6 tasks, each ~3 minutes...
Claude: /tdd   -- Starting with test for Task 1...
```

---

## Why Superpowers Works / 为什么 Superpowers 有效

**English:**

1. **Fresh subagent context per task** -- Each small task gets its own Claude session.
   This prevents the "context rot" problem where Claude's quality degrades after
   thousands of tokens of conversation.

2. **TDD ensures correctness** -- By writing tests first, Claude has a concrete
   definition of "done" for each task. No more "it looks right but doesn't work."

3. **Design before code** -- The brainstorm/spec/plan phases catch misunderstandings
   BEFORE you waste time coding the wrong thing.

**中文:**

1. **每个任务使用全新的子代理上下文** -- 每个小任务都有自己的 Claude 会话。
   这防止了"上下文腐烂"问题，即长对话后 Claude 的质量下降。

2. **TDD 确保正确性** -- 通过先写测试，Claude 对每个任务都有明确的"完成"定义。
   不再出现"看起来对但实际不工作"的情况。

3. **先设计再编码** -- 头脑风暴/规格/计划阶段在你浪费时间编写错误代码之前
   就捕获了误解。

---

## Comparison with Other Frameworks / 与其他框架的比较

| Feature / 特性 | Superpowers | GSD | GStack |
|----------------|-------------|-----|--------|
| Stars / 星标 | ~197k | ~3k | ~1k |
| Methodology / 方法论 | 7-phase structured / 7阶段结构化 | Task-focused / 任务导向 | Stack-based / 堆栈式 |
| TDD built-in / 内置TDD | Yes | No | No |
| Subagent isolation / 子代理隔离 | Yes | No | Partial / 部分 |
| Refuses premature coding / 拒绝过早编码 | Yes | No | No |
| Best for / 最适合 | Large features, teams / 大型功能、团队 | Quick tasks / 快速任务 | Layered architectures / 分层架构 |

**When to choose Superpowers / 何时选择 Superpowers:**
Use it when building non-trivial features where getting the design wrong would be
expensive. It shines on features that take more than 15 minutes.

当构建非平凡功能时使用它，如果设计错误代价高昂的话。它在需要超过 15 分钟的功能上
表现出色。

---

## Learn More / 了解更多

- GitHub: [github.com/obra/superpowers](https://github.com/obra/superpowers)
- Author: Jesse Vincent ([@obra](https://github.com/obra))
- License: MIT

---

*This document is part of the Claude Engineer examples collection.*

*本文档是 Claude Engineer 示例集的一部分。*
