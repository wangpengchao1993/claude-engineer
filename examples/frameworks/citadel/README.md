# Citadel — Multi-Agent Orchestration Harness / 多智能体编排引擎

**By [SethGammon](https://github.com/SethGammon/Citadel) | Open Source**

---

## What is Citadel? / 什么是 Citadel？

Citadel coordinates multiple AI agents working **in parallel** on your codebase.

Think of it as **a project manager who can send multiple developers to work on
different parts of the code simultaneously, then merge everything together**.

Citadel 可以协调多个 AI 智能体**并行**处理你的代码库。
你可以把它想象成一位**项目经理，能同时派多名开发者去处理代码的不同部分，然后把所有结果合并在一起**。

Most agent frameworks run one agent at a time (sequential). Citadel's key
differentiator is **true parallel execution** — multiple agents work in isolated
git worktrees at the same time, share discoveries, and merge cleanly.

大多数智能体框架一次只运行一个智能体（顺序执行）。Citadel 的核心优势是
**真正的并行执行** —— 多个智能体同时在隔离的 git worktree 中工作，共享发现，并干净地合并。

---

## Core Features / 核心功能

### 1. 4-Tier Routing (`/do`) / 四级路由

The `/do` command automatically routes your task to the cheapest and fastest
execution path based on complexity.

`/do` 命令根据任务复杂度，自动将任务路由到最经济、最快速的执行路径。

| Tier / 层级 | Description / 描述 | Example / 示例 |
|---|---|---|
| **Tier 0 — Instant** | Simple lookups, no code changes / 简单查询，无需修改代码 | "What does this function do?" |
| **Tier 1 — Single-file** | Edit one file / 编辑单个文件 | "Fix the typo in utils.py" |
| **Tier 2 — Multi-file** | Coordinated edits across files / 跨文件协调编辑 | "Add error handling to the API" |
| **Tier 3 — Fleet** | Parallel agents in worktrees / 并行智能体在工作树中 | "Implement the full auth system" |

### 2. Campaign Persistence / 战役持久化

Campaigns survive **context compression** and **session boundaries**. If your
session ends or your context window fills up, the campaign state is saved to
disk. The next session picks up exactly where you left off.

战役状态能够跨越**上下文压缩**和**会话边界**。如果会话结束或上下文窗口满了，
战役状态会保存到磁盘。下一次会话将从上次停止的地方继续。

### 3. Fleet Mode / 舰队模式

Spawn multiple agents, each in its own **isolated git worktree**. Every agent
has a full copy of the repo but works on its own branch — no merge conflicts
during work, clean integration after.

生成多个智能体，每个都在自己**隔离的 git worktree** 中运行。每个智能体拥有
完整的仓库副本，但在自己的分支上工作 —— 工作期间没有合并冲突，完成后干净集成。

### 4. Discovery Relay / 发现中继

When Agent A discovers something that Agent B needs (e.g., "the database schema
uses snake_case"), that finding is **relayed in real-time** between waves of
agents. No agent works with stale assumptions.

当智能体 A 发现了智能体 B 需要的信息（例如"数据库 schema 使用 snake_case"），
该发现会在智能体波次之间**实时中继**。没有智能体会基于过时的假设工作。

### 5. Circuit Breaker / 熔断器

If an agent runs too long, consumes too many tokens, or enters a loop, the
circuit breaker **automatically kills it** and reports what happened. This
prevents runaway costs and infinite loops.

如果一个智能体运行时间过长、消耗过多 token 或陷入循环，
熔断器会**自动终止它**并报告发生了什么。这可以防止成本失控和无限循环。

### 6. Lifecycle Hooks / 生命周期钩子

Run custom logic **before** and **after** any agent execution. Use cases:
lint checks before merge, notifications after completion, validation gates.

在任何智能体执行**之前**和**之后**运行自定义逻辑。用途包括：
合并前的 lint 检查、完成后的通知、验证关卡。

---

## 6 Production Skills / 六大生产技能

Citadel ships with 6 built-in skills optimized for real-world workflows:

Citadel 附带 6 个针对实际工作流优化的内置技能：

| Skill / 技能 | Purpose / 用途 |
|---|---|
| **`/do`** | Tier-routed task execution / 分层路由任务执行 |
| **`/campaign`** | Persistent multi-session projects / 跨会话持久化项目 |
| **`/fleet`** | Parallel agent orchestration / 并行智能体编排 |
| **`/relay`** | Cross-agent discovery sharing / 跨智能体发现共享 |
| **`/merge`** | Worktree integration and conflict resolution / 工作树集成与冲突解决 |
| **`/status`** | Campaign and fleet health dashboard / 战役与舰队健康仪表板 |

---

## Installation / 安装

Add Citadel to your Claude Code setup:

将 Citadel 添加到你的 Claude Code 配置中：

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/SethGammon/Citadel.git

# Add Citadel skills to your Claude Code settings
# 将 Citadel 技能添加到你的 Claude Code 设置中
# Follow instructions in the Citadel repo for your platform.
```

---

## Citadel vs Claude Code Harness / Citadel 与 Claude Code Harness 对比

| Feature / 功能 | Citadel | Claude Code Harness |
|---|---|---|
| Execution model / 执行模型 | **Parallel** (fleet of agents) / **并行**（智能体舰队） | **Sequential** (plan-act cycle) / **顺序**（计划-执行循环） |
| Agent isolation / 智能体隔离 | Git worktrees / Git 工作树 | Shared workspace / 共享工作区 |
| Session persistence / 会话持久化 | Campaign files on disk / 磁盘上的战役文件 | Context within session / 会话内上下文 |
| Discovery sharing / 发现共享 | Real-time relay / 实时中继 | Manual handoff / 手动交接 |
| Best for / 最适合 | Large features, team-scale / 大型功能，团队规模 | Single-agent tasks / 单智能体任务 |

Both tools are valuable. Use the Harness for focused single-agent work, and
Citadel when you need multiple agents tackling a big feature in parallel.

两种工具都有价值。使用 Harness 进行专注的单智能体工作，
当你需要多个智能体并行处理大型功能时使用 Citadel。

---

## Learn More / 了解更多

- GitHub: [github.com/SethGammon/Citadel](https://github.com/SethGammon/Citadel)
- Author: SethGammon

Scales from solo developer to institutional use.
从单人开发者到企业级使用，均可适配。
