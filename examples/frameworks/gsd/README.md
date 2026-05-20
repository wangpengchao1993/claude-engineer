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

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置要求

Before installing GSD, ensure you have the following:

安装 GSD 之前，请确保已安装以下工具：

| Requirement / 要求 | Minimum Version / 最低版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Runtime for GSD CLI / GSD CLI 运行时 |
| **npm** | 9+ | Package manager (comes with Node.js) / 包管理器（随 Node.js 附带） |
| **Claude Code CLI** | Latest | AI coding assistant / AI 编程助手 |
| **Git** | 2.30+ | Version control / 版本控制 |

#### Install prerequisites by OS / 按操作系统安装前置工具

**Windows:**

```powershell
# Install Node.js via winget
winget install OpenJS.NodeJS.LTS

# Install Git
winget install Git.Git

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**macOS:**

```bash
# Install Node.js via Homebrew
brew install node@18

# Install Git (usually pre-installed, otherwise)
brew install git

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**Linux (Ubuntu/Debian):**

```bash
# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt-get install -y git

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

### Step-by-Step Installation / 逐步安装

**Option A: Quick install (all platforms) / 快速安装（所有平台）**

```bash
# 1. Navigate to your project / 进入你的项目目录
cd your-project

# 2. Run the GSD installer / 运行 GSD 安装器
npx get-shit-done-cc

# 3. Initialize GSD in your project / 在项目中初始化 GSD
gsd init
```

**Option B: Manual install (all platforms) / 手动安装（所有平台）**

```bash
# 1. Clone the repository / 克隆仓库
git clone https://github.com/gsd-build/get-shit-done.git

# 2. Enter the directory / 进入目录
cd get-shit-done

# 3. Install dependencies / 安装依赖
npm install

# 4. Link the CLI globally / 全局链接 CLI
npm link

# 5. Go to your project / 进入你的项目
cd /path/to/your-project

# 6. Initialize GSD / 初始化 GSD
gsd init
```

### Verification / 验证安装

```bash
# Verify Node.js / 验证 Node.js
node --version
# Expected: v18.x.x or higher / 预期: v18.x.x 或更高

# Verify GSD CLI is available / 验证 GSD CLI 可用
gsd --version

# Verify Claude Code is available / 验证 Claude Code 可用
claude --version

# Verify GSD initialized correctly / 验证 GSD 初始化正确
ls .gsd/
# Expected: spec files, templates, CLAUDE.md additions
# 预期：规格文件、模板、CLAUDE.md 增补内容
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete GSD session building a REST API for a task manager app. This demonstrates how GSD keeps context fresh across the entire development cycle.

以下是使用 GSD 构建任务管理 REST API 的完整会话。演示 GSD 如何在整个开发周期中保持上下文新鲜。

### Step 1: Initialize / 第一步：初始化

```
$ cd task-manager-api
$ gsd init

> GSD initialized.
> Created: .gsd/spec.md, .gsd/tasks.md, .gsd/progress.md
> Updated: CLAUDE.md with GSD directives
> Ready to plan. Run /gsd-plan to break your idea into tasks.
```

### Step 2: Plan the work / 第二步：规划工作

```
You: /gsd-plan Build a REST API for a task manager with CRUD operations,
     user authentication, and PostgreSQL storage.

Claude: Analyzing your requirements...

  📋 Generated Task Plan (6 tasks):

  Task 1: Set up Express.js project with TypeScript configuration
  Task 2: Design and implement PostgreSQL schema with Drizzle ORM
  Task 3: Implement JWT authentication (register, login, refresh)
  Task 4: Build CRUD endpoints for tasks (/api/tasks)
  Task 5: Add input validation and error handling middleware
  Task 6: Write integration tests for all endpoints

  Dependencies: Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6
  Saved to: .gsd/tasks.md
```

### Step 3: Execute tasks with fresh sub-agents / 第三步：用全新子代理执行任务

```
You: /gsd-task 1

Claude: Spawning sub-agent for Task 1...
  ┌─────────────────────────────────────────────┐
  │ SUB-AGENT: Task 1                           │
  │ Context: task spec + project root only      │
  │ No conversation history loaded (FRESH)      │
  └─────────────────────────────────────────────┘

  Sub-agent completed:
  ✅ Created package.json with Express + TypeScript deps
  ✅ Created tsconfig.json with strict mode
  ✅ Created src/index.ts with Express boilerplate
  ✅ Created src/config/env.ts for environment variables
  Output matches spec: YES
```

**This is the key advantage** -- the sub-agent for Task 1 started with a completely fresh context. It only received the task specification and relevant file paths. No prior conversation history to pollute its thinking.

**这是关键优势** -- 任务 1 的子代理以全新上下文启动，仅接收任务规格和相关文件路径，没有历史对话污染其思维。

### Step 4: Verify task output / 第四步：验证任务输出

```
You: /gsd-verify

Claude: Running verification for Task 1...
  ✅ package.json exists and contains required dependencies
  ✅ TypeScript compiles without errors (npx tsc --noEmit)
  ✅ Express server starts and responds on port 3000
  ✅ All spec requirements for Task 1 satisfied

  Verification: PASSED
  Task 1 status: COMPLETE
```

### Step 5: Check progress / 第五步：查看进度

```
You: /gsd-status

Claude:
  ┌──────────────────────────────────────────────┐
  │ GSD Progress: task-manager-api               │
  ├──────────────────────────────────────────────┤
  │ ✅ Task 1: Express + TypeScript setup   DONE │
  │ ⬜ Task 2: PostgreSQL schema            NEXT │
  │ ⬜ Task 3: JWT authentication                │
  │ ⬜ Task 4: CRUD endpoints                    │
  │ ⬜ Task 5: Validation + error handling       │
  │ ⬜ Task 6: Integration tests                 │
  ├──────────────────────────────────────────────┤
  │ Progress: 1/6 (17%)                          │
  └──────────────────────────────────────────────┘
```

### Steps 6-10: Continue through tasks / 继续执行任务

Each subsequent `/gsd-task` call spawns a fresh sub-agent. By Task 4, a traditional AI session would be thousands of lines deep and starting to forget the auth scheme from Task 3 or the schema from Task 2. GSD sub-agents never have this problem -- each one reads directly from the spec files.

每次后续的 `/gsd-task` 调用都会生成全新的子代理。到任务 4 时，传统 AI 会话已有数千行之深，开始遗忘任务 3 的认证方案或任务 2 的数据库模式。GSD 子代理永远不会有这个问题——每个子代理直接从规格文件读取。

### Step 11: Finish / 最后一步：收尾

```
You: /gsd-finish

Claude: Running final checks...
  ✅ All 6 tasks verified
  ✅ TypeScript compiles cleanly
  ✅ All 24 integration tests pass
  ✅ No lint errors

  📊 Summary:
  - 6 tasks completed across 6 focused sub-agent sessions
  - 12 files created, 0 spec violations
  - Total tokens used per sub-agent: ~4,000 (vs ~45,000 in a single session)
  - Context freshness maintained throughout

  GSD session complete. Your code is ready.
```

### Why This Matters: Context Freshness / 为什么这很重要：上下文新鲜度

```
Traditional session (no GSD):          GSD session:
Token 0     ████████ 100% accuracy     Task 1  ████████ 100% accuracy
Token 5K    ███████░  90% accuracy     Task 2  ████████ 100% accuracy
Token 15K   █████░░░  70% accuracy     Task 3  ████████ 100% accuracy
Token 30K   ███░░░░░  50% accuracy     Task 4  ████████ 100% accuracy
Token 50K   █░░░░░░░  30% accuracy     Task 5  ████████ 100% accuracy
                                       Task 6  ████████ 100% accuracy
```

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| `gsd: command not found` | CLI not linked globally / CLI 未全局链接 | Run `npm link` in the get-shit-done directory, or use `npx get-shit-done-cc` / 在 get-shit-done 目录运行 `npm link`，或使用 `npx get-shit-done-cc` |
| `gsd init` fails with permission error | No write permission in project directory / 项目目录无写入权限 | Check directory permissions: `ls -la .` / 检查目录权限 |
| Sub-agent does not spawn | Claude Code CLI not installed or not authenticated / Claude Code CLI 未安装或未认证 | Run `claude --version` to verify installation, then `claude login` / 运行 `claude --version` 验证安装，然后 `claude login` |
| `/gsd-plan` produces empty task list | Vague or missing project description / 项目描述模糊或缺失 | Provide a clear, specific description of what you want to build / 提供清晰具体的构建需求描述 |
| Verification fails unexpectedly | Spec file out of sync with actual changes / 规格文件与实际改动不同步 | Run `gsd init` to regenerate specs, then re-plan / 运行 `gsd init` 重新生成规格，然后重新规划 |
| `npm link` fails on Windows | PowerShell execution policy restriction / PowerShell 执行策略限制 | Run PowerShell as Administrator, or use `npx get-shit-done-cc` instead / 以管理员身份运行 PowerShell，或改用 `npx get-shit-done-cc` |
| Node.js version too old | Node.js < 18 installed / 安装了 Node.js 18 以下版本 | Update Node.js: `nvm install 18` or download from nodejs.org / 更新 Node.js |
| `.gsd/` directory not created | Running `gsd init` outside a git repo / 在 git 仓库外运行 `gsd init` | Initialize git first: `git init` then `gsd init` / 先初始化 git：`git init` 再 `gsd init` |

---

*This README is part of the Claude Engineer frameworks collection.*

*本 README 是 Claude Engineer 框架合集的一部分。*
