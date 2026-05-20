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

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置条件

| Requirement / 要求 | Version / 版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Runtime for Claude Code / Claude Code 运行时 |
| **Claude Code CLI** | Latest / 最新 | AI coding assistant / AI 编码助手 |
| **Git** | 2.30+ | Version control & worktrees / 版本控制与工作树 |

#### Install Prerequisites / 安装前置条件

**Windows:**
```powershell
# Install Node.js via winget / 通过 winget 安装 Node.js
winget install OpenJS.NodeJS.LTS

# Install Git (worktree support requires 2.30+) / 安装 Git（工作树支持需要 2.30+）
winget install Git.Git

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**macOS:**
```bash
# Install via Homebrew / 通过 Homebrew 安装
brew install node@18 git

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**Linux (Ubuntu/Debian):**
```bash
# Install Node.js 18+ / 安装 Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs git

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

### Step-by-Step Installation / 分步安装

```bash
# 1. Clone Citadel into your project's .claude/ directory
#    将 Citadel 克隆到项目的 .claude/ 目录
cd your-project
git clone https://github.com/SethGammon/Citadel.git .claude/citadel

# 2. Copy skill definitions into Claude Code config
#    将技能定义复制到 Claude Code 配置中
cp .claude/citadel/skills/*.md .claude/skills/

# 3. Add Citadel commands to your Claude Code settings
#    将 Citadel 命令添加到 Claude Code 设置中
cat .claude/citadel/settings-snippet.json >> .claude/settings.json

# 4. Verify by launching Claude Code / 启动 Claude Code 验证
claude
> /status
# Should show: "Citadel v1.x — 6 skills loaded, fleet mode available"
# 应显示: "Citadel v1.x — 6 skills loaded, fleet mode available"
```

### Verification / 验证

```bash
# Check all components / 检查所有组件
node --version          # Should be v18.x or higher / 应为 v18.x 或更高
git --version           # Should be 2.30+ / 应为 2.30+
claude --version        # Should show Claude Code CLI version / 应显示 Claude Code CLI 版本
git worktree list       # Should work without errors / 应无报错运行

# Inside Claude Code / 在 Claude Code 内部
claude
> /do "hello world"     # Should route to Tier 0 and respond / 应路由到 Tier 0 并响应
> /status               # Should show Citadel dashboard / 应显示 Citadel 仪表板
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete session showing Citadel building a full authentication system with parallel agents.

以下是一个完整的会话演示，展示 Citadel 如何用并行智能体构建一个完整的认证系统。

### Step 1: Initiate the Task with /do / 步骤1：使用 /do 发起任务

```
$ claude
> /do build authentication system with JWT tokens, login/signup UI,
  and comprehensive test coverage

Citadel [routing] Analyzing task complexity...
  - Code changes required: API routes, middleware, UI components, tests
  - Files affected: ~25-30 across 4 directories
  - Dependencies between components: auth-api ↔ auth-ui ↔ auth-tests

Citadel [routing] Complexity: TIER 3 — FLEET MODE
  This task requires parallel agents in isolated worktrees.

Proceed with Tier 3 fleet execution? (y/n): y
```

### Step 2: Campaign Created and Persisted / 步骤2：创建并持久化战役

```
Citadel [campaign] Creating campaign: "auth-system-20260520"
  - Campaign file: .claude/citadel/campaigns/auth-system-20260520.json
  - Status: ACTIVE
  - Estimated agents: 3
  - Estimated duration: 8-12 minutes

Campaign persisted to disk. If this session ends, resume with:
  /campaign resume auth-system-20260520

战役已持久化到磁盘。如果此会话结束，可通过以下命令恢复：
  /campaign resume auth-system-20260520
```

### Step 3: Fleet Mode — 3 Agents Spawn in Isolated Worktrees / 步骤3：舰队模式 — 3 个智能体在隔离工作树中生成

```
Citadel [fleet] Spawning 3 agents in isolated git worktrees...

  Agent 1: auth-api
    Branch: citadel/auth-api-20260520
    Worktree: .worktrees/auth-api/
    Task: Implement JWT authentication endpoints
      - POST /api/auth/login
      - POST /api/auth/signup
      - POST /api/auth/refresh
      - GET  /api/auth/me
      - Auth middleware with token validation

  Agent 2: auth-ui
    Branch: citadel/auth-ui-20260520
    Worktree: .worktrees/auth-ui/
    Task: Build login/signup UI components
      - LoginForm component
      - SignupForm component
      - AuthProvider context
      - Protected route wrapper
      - Token storage utilities

  Agent 3: auth-tests
    Branch: citadel/auth-tests-20260520
    Worktree: .worktrees/auth-tests/
    Task: Write comprehensive test suite
      - Unit tests for auth endpoints
      - Integration tests for login flow
      - UI component tests
      - Token refresh edge cases

All 3 agents working in parallel...
```

### Step 4: Discovery Relay — Agents Share Findings / 步骤4：发现中继 — 智能体共享发现

```
Citadel [relay] Agent auth-api published discovery:
  {
    "type": "schema",
    "content": "JWT token payload: { userId: string, email: string,
                role: 'admin'|'user', exp: number }",
    "source": "auth-api"
  }

Citadel [relay] → Relayed to auth-ui
  auth-ui agent now knows the exact token schema and will decode
  tokens correctly in the AuthProvider.

Citadel [relay] → Relayed to auth-tests
  auth-tests agent now knows the expected token payload structure
  for assertion matching.

Citadel [relay] Agent auth-api published discovery:
  {
    "type": "endpoint",
    "content": "POST /api/auth/login returns { token, refreshToken, user }",
    "source": "auth-api"
  }

Citadel [relay] → Relayed to auth-ui, auth-tests
```

### Step 5: Circuit Breaker — Stuck Agent Killed / 步骤5：熔断器 — 卡住的智能体被终止

```
Citadel [monitor] Agent health check:
  auth-api:   ████████████████████ COMPLETE (4m 22s)
  auth-ui:    ██████████████████░░ 90% (5m 10s)
  auth-tests: ████████░░░░░░░░░░░░ 40% (5m 10s) ⚠ SLOW

Citadel [circuit-breaker] WARNING: auth-tests exceeded time threshold
  - Elapsed: 5m 10s / Budget: 6m 00s
  - Token consumption: 45k / Budget: 50k
  - Agent appears to be in a retry loop on integration tests

... (50 seconds later / 50 秒后)

Citadel [circuit-breaker] TRIPPED: auth-tests killed after 6m 00s
  - Reason: exceeded time budget
  - Partial work saved to branch citadel/auth-tests-20260520
  - 8/14 test files completed before termination
  - Recovery: remaining 6 test files flagged for manual completion

Citadel [fleet] Fleet status:
  auth-api:   ✓ COMPLETE
  auth-ui:    ✓ COMPLETE
  auth-tests: ⚠ PARTIAL (8/14 files, circuit breaker tripped)
```

### Step 6: Results Merged into Main Branch / 步骤6：结果合并到主分支

```
Citadel [merge] Merging completed agent work into main branch...

  Step 1/3: Merge auth-api → main
    ✓ 6 files added, 2 files modified
    ✓ No conflicts

  Step 2/3: Merge auth-ui → main
    ✓ 8 files added, 1 file modified
    ✓ No conflicts (relay data prevented schema mismatch)

  Step 3/3: Merge auth-tests (partial) → main
    ✓ 8 test files added
    ⚠ 6 test files still pending (see campaign notes)
    ✓ No conflicts

Citadel [merge] Integration complete.
  Files added:   22
  Files modified: 3
  Conflicts:     0
  Test coverage:  auth-api 100%, auth-ui 100%, auth-tests 57% (partial)

Campaign "auth-system-20260520" status: COMPLETE (with notes)
  Note: 6 remaining test files need manual completion.
  Run `/do complete auth-tests remaining test files` to finish.
```

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| `/do` command not recognized | Citadel skills not loaded | Re-copy skills: `cp .claude/citadel/skills/*.md .claude/skills/` / 重新复制技能文件 |
| `git worktree add` fails | Not inside a git repository | Run `git init` first, or ensure you are in a git repo / 先运行 `git init`，或确保在 git 仓库中 |
| Fleet agents fail to spawn | Git version too old for worktrees | Upgrade Git to 2.30+: `git --version` to check / 升级 Git 到 2.30+：用 `git --version` 检查 |
| Merge conflicts after fleet | Agents modified same files | Use `/merge --interactive` to resolve manually / 使用 `/merge --interactive` 手动解决 |
| Campaign not resuming | Campaign file corrupted | Check `.claude/citadel/campaigns/` for the JSON file; delete and re-run / 检查 JSON 文件；删除后重新运行 |
| Circuit breaker trips too early | Default timeout too short | Edit `.claude/citadel/config.json` — increase `circuit_breaker.timeout_seconds` / 增加 `circuit_breaker.timeout_seconds` |
| Discovery relay not working | Agents in different worktrees cannot communicate | Ensure `.claude/citadel/relay/` directory exists and is writable / 确保 relay 目录存在且可写 |
| `/status` shows no agents | Fleet mode not activated | Use `/do` with a Tier 3 task, or explicitly run `/fleet spawn` / 使用 Tier 3 任务的 `/do`，或显式运行 `/fleet spawn` |
| Worktrees not cleaned up | Session ended before cleanup | Run `git worktree list` then `git worktree remove <path>` for stale entries / 运行 `git worktree list` 后移除旧条目 |

---

## Learn More / 了解更多

- GitHub: [github.com/SethGammon/Citadel](https://github.com/SethGammon/Citadel)
- Author: SethGammon

Scales from solo developer to institutional use.
从单人开发者到企业级使用，均可适配。
