# GSD -- Get Shit Done / 把事做完框架

> ~60k stars | By TACHES | MIT License
>
> ~60k 星 | 作者 TACHES | MIT 许可证

---

## What is GSD? / GSD 是什么?

GSD is a lightweight meta-prompting, context engineering, and spec-driven development
system built entirely on **Claude Code's native features** -- slash commands, CLAUDE.md,
hooks, and agent spawning. No proprietary runtime. No framework dependency. Just ~50
Markdown files and a small Node.js CLI helper that orchestrate the complete development
cycle from idea to delivered code.

GSD 是一个轻量级的元提示、上下文工程与规格驱动开发系统，完全基于 **Claude Code 原生功能**
构建 -- 斜杠命令、CLAUDE.md、钩子和子代理生成。没有私有运行时，没有框架依赖。
仅用约 50 个 Markdown 文件和一个小型 Node.js CLI 工具，编排从创意到交付代码的完整开发周期。

**Think of it as a GPS for your AI coding session -- it always knows where you are and
where you're going.**

**可以把它想象成 AI 编程会话的 GPS -- 它始终知道你在哪里、要去哪里。**

Trusted by engineers at Amazon, Google, Shopify, and Webflow.

已获得 Amazon、Google、Shopify 和 Webflow 工程师的信赖。

---

## The Problem: Context Rot / 问题：上下文腐烂

After thousands of lines of conversation, AI coding assistants start to degrade:

经过数千行对话后，AI 编程助手开始退化：

- **Forgets specifications** -- requirements from earlier in the session quietly disappear.
  **忘记规格** -- 会话早期的需求悄然消失。
- **Generates inconsistent code** -- naming conventions drift, patterns contradict earlier decisions.
  **生成不一致的代码** -- 命名规范漂移，模式与早期决策矛盾。
- **Loses track of logic** -- the AI no longer understands how components connect.
  **丢失逻辑线索** -- AI 不再理解组件之间的关联。

This is **context rot**: accuracy degrades as the session grows. It is the #1 problem
in AI-assisted coding today.

这就是**上下文腐烂**：随着会话增长，准确性不断下降。这是当今 AI 辅助编程的头号问题。

---

## How GSD Solves It / GSD 如何解决

GSD breaks long sessions into **short, focused sub-agent tasks**. Each sub-agent spawns
with a fresh context containing only the task specification and relevant files -- not the
entire conversation history. After each sub-agent completes, automatic verification
confirms the work matches the spec.

GSD 将长会话拆分为**短小、聚焦的子代理任务**。每个子代理以全新的上下文启动，
仅包含任务规格和相关文件 -- 而非完整的对话历史。每个子代理完成后，自动验证确认
工作符合规格。

**Specialized sub-agents + fresh contexts + automatic verification = no more context rot.**

**专用子代理 + 全新上下文 + 自动验证 = 不再有上下文腐烂。**

---

## The Core Loop: 6 Commands / 核心循环：6 个命令

Each command does exactly one thing. Together they form a complete development cycle.

每个命令只做一件事。组合在一起形成完整的开发周期。

| # | Command / 命令 | What it does / 功能 |
|---|----------------|---------------------|
| 1 | `/gsd-init`    | Initialize project structure and specs / 初始化项目结构与规格 |
| 2 | `/gsd-plan`    | Break work into small, testable tasks / 将工作拆分为可测试的小任务 |
| 3 | `/gsd-task`    | Spawn a sub-agent for one focused task / 为一个聚焦任务生成子代理 |
| 4 | `/gsd-verify`  | Automatically verify task output against spec / 自动验证任务输出是否符合规格 |
| 5 | `/gsd-status`  | Show progress across all tasks / 显示所有任务的进度 |
| 6 | `/gsd-finish`  | Wrap up, run final checks, generate summary / 收尾、最终检查、生成总结 |

---

## How It Works Under the Hood / 底层工作原理

```
Your idea / 你的想法
    |
    v
  /gsd-init  -->  CLAUDE.md + spec files (~50 Markdown files)
    |                 ~50 个 Markdown 文件
    v
  /gsd-plan  -->  Task list with dependencies
    |                 带依赖关系的任务列表
    v
  /gsd-task  -->  Fresh sub-agent (focused context only)
    |                 全新子代理（仅聚焦上下文）
    v
  /gsd-verify -->  Automatic spec conformance check
    |                 自动规格符合性检查
    v
  (repeat for each task / 对每个任务重复)
    |
    v
  /gsd-finish -->  Delivered code
                      交付代码
```

Components / 组件:

- **~50 Markdown files**: Specifications, templates, checklists -- the "memory" that
  persists across sub-agents. / 规格、模板、清单 -- 跨子代理持久化的"记忆"。
- **Node.js CLI** (`gsd` command): Lightweight orchestrator for spawning sub-agents and
  managing task state. / 轻量级编排器，用于生成子代理和管理任务状态。
- **Hooks**: Claude Code hooks that trigger verification automatically after each task.
  / Claude Code 钩子，在每个任务后自动触发验证。

---

## Installation / 安装

### Quick install / 快速安装

```bash
npx get-shit-done-cc
```

### Manual setup / 手动安装

```bash
git clone https://github.com/gsd-build/get-shit-done.git
cd get-shit-done
npm install
npm link
```

Then in your project / 然后在你的项目中:

```bash
gsd init
```

---

## Key Differentiator / 核心差异

GSD is the **lightest-weight** of all AI coding frameworks:

GSD 是所有 AI 编程框架中**最轻量级**的：

- **No framework dependency** -- uses only Claude Code native features (slash commands,
  CLAUDE.md, hooks, agent spawning). / **无框架依赖** -- 仅使用 Claude Code 原生功能。
- **No proprietary runtime** -- everything is Markdown files and standard Node.js.
  / **无私有运行时** -- 全部是 Markdown 文件和标准 Node.js。
- **No lock-in** -- remove GSD and your project still works perfectly.
  / **无锁定** -- 移除 GSD，你的项目仍完美运行。

---

## GSD vs Superpowers / GSD 与 Superpowers 对比

| Aspect / 方面          | GSD                          | Superpowers                     |
|------------------------|------------------------------|---------------------------------|
| Weight / 重量           | Ultra-light (~50 .md + CLI)  | Heavier (more tooling)          |
| Philosophy / 理念       | Minimal, convention-based    | Structured, config-driven       |
| Context strategy / 上下文策略 | Fresh sub-agents per task  | Persistent enhanced context     |
| Setup / 安装            | One command                  | More configuration              |
| Best for / 最适合       | Fast iteration, small teams  | Large teams, complex workflows  |

Both are excellent. GSD is lighter and closer to vanilla Claude Code. Superpowers
provides more structure and guardrails.

两者都很出色。GSD 更轻量，更接近原生 Claude Code。Superpowers 提供更多结构和护栏。

---

## Learn More / 了解更多

- GitHub: [github.com/gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
- License: MIT

---

*This README is part of the Claude Engineer frameworks collection.*

*本 README 是 Claude Engineer 框架合集的一部分。*
