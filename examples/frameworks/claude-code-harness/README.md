# Claude Code Harness — Autonomous Plan->Work->Review Cycle / 自治的计划->开发->审查循环

**By [Chachamaru127](https://github.com/Chachamaru127/claude-code-harness) | Open Source**

---

## What is it? / 这是什么?

Claude Code Harness turns Claude Code's raw capability into a **trustworthy delivery loop**.
Think of it as "putting guardrails on a powerful car — same speed, much safer."

Claude Code Harness 将 Claude Code 的原始能力转化为一个**可信赖的交付循环**。
可以把它想象成"给一辆强大的跑车装上护栏 -- 同样的速度，更加安全。"

Without Harness, Claude Code is powerful but unstructured. With Harness, every change goes through a disciplined cycle:

没有 Harness 时，Claude Code 强大但缺乏结构。有了 Harness，每个变更都经过严格的循环：

```
Plan -> Parallel Implementation -> Review -> Commit
计划 -> 并行实现 -> 审查 -> 提交
```

After you approve the plan, **one command** drives the entire cycle to completion.

批准计划后，**一条命令**即可驱动整个循环到完成。

---

## Core Cycle / 核心循环

```
  [Plan]          Create a detailed task list from requirements
   计划            根据需求创建详细任务列表
     |
     v
  [Work]          Worker agents implement tasks in parallel
   开发            工作代理并行实现任务
     |
     v
  [Guardrail]     Go engine validates every change (<10ms)
   护栏检查        Go 引擎验证每个变更（<10ms）
     |
     v
  [Review]        Reviewer agent checks quality against plan
   审查            审查代理对照计划检查质量
     |
     v
  [Commit]        Auto-commit if all checks pass
   提交            所有检查通过后自动提交
```

---

## 5 Verb Skills / 五个动词技能

Harness organizes everything around **5 simple verbs**:

Harness 围绕**5个简单动词**组织一切：

| Verb / 动词 | What it does / 作用 | Example / 示例 |
|---|---|---|
| **setup** | Configure project rules and guardrails / 配置项目规则和护栏 | `harness setup --lang python` |
| **plan** | Create an implementation plan from requirements / 根据需求创建实施计划 | `harness plan "add user auth"` |
| **work** | Implement tasks via worker agents / 通过工作代理实现任务 | `harness work` |
| **review** | Verify implementation against plan / 对照计划验证实现 | `harness review` |
| **release** | Ship it (create PR, tag, etc.) / 发布（创建PR、标签等） | `harness release` |

---

## 3 Agents / 三个代理

| Agent / 代理 | Role / 角色 |
|---|---|
| **Worker** | Implements code changes according to the plan / 根据计划实现代码变更 |
| **Reviewer** | Checks quality, correctness, and plan adherence / 检查质量、正确性和计划一致性 |
| **Scaffolder** | Creates boilerplate, file structures, and templates / 创建样板代码、文件结构和模板 |

---

## Go-Native Guardrail Engine / Go 原生护栏引擎

The **key differentiator** of Harness is its Go-native guardrail engine:

Harness 的**核心差异化特性**是其 Go 原生护栏引擎：

- **Sub-10ms response** — checks happen so fast they never slow you down
  **亚10毫秒响应** -- 检查速度极快，绝不拖慢你的节奏
- **Prevents mistakes before they happen** — not just review after the fact
  **在错误发生前预防** -- 不只是事后审查
- **Protects execution** — blocks forbidden patterns, enforces file boundaries, validates imports
  **保护执行过程** -- 阻止禁止模式、强制文件边界、验证导入

Example: if your guardrails say "never modify database migrations directly," the engine blocks
that change in under 10ms — before Claude Code even writes the file.

例如：如果你的护栏规则说"绝不直接修改数据库迁移"，引擎会在10ms内阻止
该变更 -- 甚至在 Claude Code 写入文件之前。

---

## Installation & Setup / 安装与设置

```bash
# 1. Clone the repository / 克隆仓库
git clone https://github.com/Chachamaru127/claude-code-harness.git
cd claude-code-harness

# 2. Install dependencies / 安装依赖
#    The Go guardrail engine compiles automatically
#    Go 护栏引擎会自动编译
make install

# 3. Initialize in your project / 在你的项目中初始化
cd your-project
harness setup --lang python

# 4. Create a plan / 创建计划
harness plan "add user authentication with JWT"

# 5. Review the plan, then execute / 审查计划，然后执行
harness work     # implements all tasks / 实现所有任务
harness review   # checks everything / 检查所有内容
harness release  # ships it / 发布
```

---

## CLI Entry Point / CLI 入口

Harness provides a single `harness` command as your entry point:

Harness 提供单一的 `harness` 命令作为入口：

```bash
harness <verb> [options]

# Examples / 示例:
harness setup --lang go --guardrails strict
harness plan "refactor auth module"
harness work --parallel 3
harness review --verbose
harness release --pr --tag v1.2.0
```

---

## Comparison with GSD / 与 GSD 的对比

| Feature / 特性 | Claude Code Harness | GSD |
|---|---|---|
| Guardrail engine / 护栏引擎 | Go-native, sub-10ms / Go 原生，亚10ms | None (pure Markdown) / 无（纯 Markdown） |
| Prevention vs. detection / 预防 vs 检测 | Prevents before execution / 执行前预防 | Reviews after execution / 执行后审查 |
| Agent system / 代理系统 | Worker + Reviewer + Scaffolder | Task-based agents / 基于任务的代理 |
| Language / 语言 | Go + Claude Code | Pure Markdown / 纯 Markdown |
| Speed overhead / 速度开销 | <10ms per check / 每次检查<10ms | N/A |

Both are excellent frameworks. Choose Harness when you need **runtime safety guarantees**;
choose GSD when you want a **lightweight, zero-dependency** approach.

两者都是优秀的框架。当你需要**运行时安全保障**时选择 Harness；
当你想要**轻量级、零依赖**的方式时选择 GSD。

---

## Learn More / 了解更多

- GitHub: [github.com/Chachamaru127/claude-code-harness](https://github.com/Chachamaru127/claude-code-harness)

---

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置条件

| Requirement / 要求 | Version / 版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Runtime for Claude Code / Claude Code 运行时 |
| **Claude Code CLI** | Latest / 最新 | AI coding assistant / AI 编码助手 |
| **Git** | 2.30+ | Version control / 版本控制 |
| **Go** | 1.21+ | Guardrail engine compilation / 护栏引擎编译 |
| **Make** | Any | Build automation / 构建自动化 |

#### Install Prerequisites / 安装前置条件

**Windows:**
```powershell
# Install Node.js via winget / 通过 winget 安装 Node.js
winget install OpenJS.NodeJS.LTS

# Install Git / 安装 Git
winget install Git.Git

# Install Go / 安装 Go
winget install GoLang.Go

# Install Make (via Chocolatey) / 通过 Chocolatey 安装 Make
choco install make

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**macOS:**
```bash
# Install via Homebrew / 通过 Homebrew 安装
brew install node@18 git go make

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

**Linux (Ubuntu/Debian):**
```bash
# Install Node.js 18+, Git, Go, Make / 安装 Node.js 18+, Git, Go, Make
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs git golang-go make

# Install Claude Code CLI / 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

### Step-by-Step Installation / 分步安装

```bash
# 1. Clone the Harness repository / 克隆 Harness 仓库
git clone https://github.com/Chachamaru127/claude-code-harness.git
cd claude-code-harness

# 2. Install and build (compiles the Go guardrail engine)
#    安装并构建（编译 Go 护栏引擎）
make install

# 3. Navigate to your project / 进入你的项目目录
cd /path/to/your-project

# 4. Initialize Harness for your project / 为你的项目初始化 Harness
harness setup --lang python    # or: go, javascript, typescript, rust
                               # 或者: go, javascript, typescript, rust

# 5. Verify the setup / 验证安装
harness --version
# Should show: claude-code-harness v1.x.x (guardrail engine: go1.21+)
# 应显示: claude-code-harness v1.x.x (guardrail engine: go1.21+)
```

### Verification / 验证

```bash
# Check all components / 检查所有组件
node --version          # Should be v18.x or higher / 应为 v18.x 或更高
go version              # Should be 1.21+ / 应为 1.21+
claude --version        # Should show Claude Code CLI version / 应显示 Claude Code CLI 版本
harness --version       # Should show Harness version with guardrail engine / 应显示 Harness 版本及护栏引擎

# Test guardrail engine / 测试护栏引擎
harness setup --check
# Should show: "Guardrail engine: OK (sub-10ms response)"
# 应显示: "Guardrail engine: OK (sub-10ms response)"
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete session showing the Plan, Work, Review cycle with real guardrail enforcement.

以下是一个完整的会话演示，展示计划、开发、审查循环以及真实的护栏执行。

### Step 1: /harness setup — Configure Project / 步骤1：配置项目

```
$ cd my-web-app
$ harness setup --lang python --guardrails strict

Harness [setup] Scanning project structure...
  - Language: Python
  - Framework detected: FastAPI
  - Test runner detected: pytest
  - Guardrail level: strict

Harness [setup] Writing configuration to .harness/config.yaml
  Guardrails enabled:
    ✓ No hardcoded secrets (API keys, passwords, tokens)
    ✓ No direct database migration modifications
    ✓ No imports from banned packages
    ✓ All functions must have type hints
    ✓ No files > 500 lines
    ✓ Test files required for new modules

Harness [setup] Go guardrail engine compiled and ready.
  Response time: 3ms average per check.

Setup complete. Run `harness plan "<requirement>"` to start.
```

### Step 2: /harness plan — Create Implementation Plan / 步骤2：创建实现计划

```
$ harness plan "add user authentication with JWT, including login,
  signup, password reset, and role-based access control"

Harness [plan] Analyzing requirement...
  - Complexity: MEDIUM (6-10 tasks)
  - Affected areas: API routes, models, middleware, tests

Harness [plan] Implementation plan created:

  Task 1: Create User model with password hashing
  Task 2: Implement JWT token generation and validation utilities
  Task 3: Build POST /auth/signup endpoint
  Task 4: Build POST /auth/login endpoint
  Task 5: Build POST /auth/password-reset endpoint
  Task 6: Implement role-based access control middleware
  Task 7: Add protected route decorators
  Task 8: Write comprehensive test suite

  Plan saved to: .harness/plans/auth-20260520.yaml

Review the plan above. Approve? (y/n): y

Plan approved. Run `harness work` to begin implementation.
```

### Step 3: /harness work — Parallel Workers Implement Tasks / 步骤3：并行工人实现任务

```
$ harness work

Harness [work] Spawning 3 parallel worker agents...

  Worker 1: Tasks 1-3 (User model, JWT utils, signup)
  Worker 2: Tasks 4-6 (login, password reset, RBAC middleware)
  Worker 3: Tasks 7-8 (route decorators, tests)

  Worker 1: ████████████████████ Task 1 COMPLETE — models/user.py created
  Worker 1: ████████████████████ Task 2 COMPLETE — utils/jwt.py created
  Worker 2: ████████████████████ Task 4 COMPLETE — routes/auth.py (login)
  Worker 1: ████████████████████ Task 3 COMPLETE — routes/auth.py (signup)
  Worker 2: ████████████████████ Task 5 COMPLETE — routes/auth.py (reset)
```

### Step 4: Guardrail Blocks a Bad Change / 步骤4：护栏阻止了一个错误变更

```
  Worker 2: Implementing Task 6 (RBAC middleware)...

  Harness [guardrail] ✗ BLOCKED — Worker 2, file: middleware/auth.py
    Rule violated: NO_HARDCODED_SECRETS
    Line 14: JWT_SECRET = "my-super-secret-key-12345"
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Hardcoded secret detected. Use environment variable instead.

    Suggestion: Replace with `os.environ.get("JWT_SECRET")`
    Response time: 2ms

  Worker 2: [auto-correcting] Replacing hardcoded secret...
    - JWT_SECRET = "my-super-secret-key-12345"
    + JWT_SECRET = os.environ.get("JWT_SECRET")
    + if not JWT_SECRET:
    +     raise RuntimeError("JWT_SECRET environment variable not set")

  Harness [guardrail] ✓ PASSED — middleware/auth.py (re-check: 3ms)

  Worker 2: ████████████████████ Task 6 COMPLETE — middleware/auth.py
  Worker 3: ████████████████████ Task 7 COMPLETE — decorators/auth.py
  Worker 3: ████████████████████ Task 8 COMPLETE — tests/test_auth.py

Harness [work] All 8 tasks completed.
  Files created: 7
  Files modified: 2
  Guardrail checks: 34 total, 1 blocked and auto-corrected
```

### Step 5: /harness review — Reviewer Agent Checks Work / 步骤5：审查代理检查工作

```
$ harness review

Harness [review] Reviewer agent analyzing implementation against plan...

  Checking Task 1 (User model): ✓ Matches plan
    - Password hashing with bcrypt: present
    - Email validation: present
    - Role field with enum: present

  Checking Task 2 (JWT utils): ✓ Matches plan
  Checking Task 3 (Signup): ✓ Matches plan
  Checking Task 4 (Login): ✓ Matches plan
  Checking Task 5 (Password reset): ✓ Matches plan
  Checking Task 6 (RBAC middleware): ✓ Matches plan
    Note: guardrail caught a hardcoded secret — auto-corrected
  Checking Task 7 (Route decorators): ✓ Matches plan
  Checking Task 8 (Tests): ✓ Matches plan

  Running test suite: pytest tests/test_auth.py
    ✓ 24 tests passed, 0 failed

Harness [review] APPROVED — All 8 tasks match plan, all tests pass.
```

### Step 6: /harness release — Ship the PR / 步骤6：发布 PR

```
$ harness release --pr --tag v1.3.0

Harness [release] Preparing release...
  ✓ All guardrail checks passing
  ✓ All tests passing (24/24)
  ✓ Review: APPROVED

  Creating branch: feature/auth-system
  Committing 9 files with message:
    "feat: add JWT authentication with RBAC

     - User model with bcrypt password hashing
     - JWT token generation/validation
     - Login, signup, password reset endpoints
     - Role-based access control middleware
     - 24 tests with full coverage"

  Creating pull request...
  ✓ PR #47 created: "Add JWT authentication with RBAC"
    https://github.com/your-org/my-web-app/pull/47

  Tagging: v1.3.0
  ✓ Tag created

Harness [release] Done. PR #47 is ready for human review.
```

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| `make install` fails | Go not installed or not in PATH | Install Go 1.21+: check with `go version` / 安装 Go 1.21+：用 `go version` 检查 |
| `harness setup` not found | Harness binary not in PATH | Add to PATH: `export PATH=$PATH:$(go env GOPATH)/bin` / 添加到 PATH |
| Guardrail engine not responding | Go binary not compiled | Run `make install` again in the harness repo / 在 harness 仓库中重新运行 `make install` |
| `harness plan` produces empty plan | Requirement too vague | Provide more detail: include specific endpoints, models, or behaviors / 提供更多细节 |
| Worker agent hangs | Claude Code CLI session expired | Re-authenticate with `claude login` / 用 `claude login` 重新认证 |
| Guardrail false positive | Rule too strict for your project | Edit `.harness/config.yaml` to adjust rules / 编辑 `.harness/config.yaml` 调整规则 |
| `harness review` fails | Tests not configured | Ensure test runner is set in `.harness/config.yaml` / 确保在配置中设置了测试运行器 |
| `harness release --pr` fails | No GitHub remote configured | Run `git remote add origin <url>` first / 先运行 `git remote add origin <url>` |
| Permission denied on Linux | Binary lacks execute permission | Run `chmod +x $(which harness)` / 运行 `chmod +x $(which harness)` |

---

*Harness does not replace Claude Code — it makes Claude Code safer and more structured.*

*Harness 不是替代 Claude Code -- 它让 Claude Code 更安全、更有结构。*
