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

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置条件

| Requirement / 要求 | Version / 版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Runtime for Claude Code / Claude Code 运行时 |
| **Claude Code CLI** | Latest / 最新 | AI coding assistant / AI 编码助手 |
| **Git** | 2.30+ | Version control / 版本控制 |

#### Install Prerequisites / 安装前置条件

**Windows:**
```powershell
# Install Node.js via winget / 通过 winget 安装 Node.js
winget install OpenJS.NodeJS.LTS

# Install Git / 安装 Git
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
# 1. Launch Claude Code / 启动 Claude Code
claude

# 2. Install the plugin from marketplace / 从市场安装插件
> /plugin marketplace add shinpr/claude-code-workflows

# Output / 输出:
# ✓ Downloaded claude-code-workflows v1.x.x
# ✓ Registered workflow commands
# ✓ Agents configured: Requirement, Design, Implementation, Quality
# Plugin claude-code-workflows installed successfully.

# 3. (Optional) Install companion plugins / （可选）安装配套插件
> /plugin marketplace add shinpr/claude-code-workflows-discover
> /plugin marketplace add shinpr/claude-code-workflows-metronome
```

### Verification / 验证

```bash
# Check all components / 检查所有组件
node --version          # Should be v18.x or higher / 应为 v18.x 或更高
claude --version        # Should show Claude Code CLI version / 应显示 Claude Code CLI 版本

# Inside Claude Code / 在 Claude Code 内部
claude
> /plugin list
# Should show: claude-code-workflows v1.x.x (active)
# 应显示: claude-code-workflows v1.x.x (active)

> /workflow status
# Should show: "Workflows ready — 4 agents available"
# 应显示: "Workflows ready — 4 agents available"
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete session showing the full lifecycle for building a "user authentication" feature.

以下是一个完整的会话演示，展示构建"用户认证"功能的完整生命周期。

### Step 1: Complexity Analysis / 步骤1：复杂度分析

```
$ claude
> Build a user authentication system with login, signup,
  password reset, and session management

Workflows [requirement-agent] Analyzing task complexity...
  Scanning codebase: 142 files, FastAPI backend, React frontend
  Evaluating scope: API endpoints + UI screens + session logic

Workflows [requirement-agent] Complexity: MEDIUM
  - Estimated tasks: 8
  - Pipeline: Full (PRD → UI Spec → Design Doc → Work Plan → Implementation)
  - Reason: Multiple API endpoints + UI screens + cross-cutting session logic

Starting full lifecycle pipeline...
```

### Step 2: PRD Auto-Generated / 步骤2：PRD 自动生成

```
Workflows [design-agent] Generating PRD...

  PRD: User Authentication System
  ================================
  1. Overview
     Add complete user authentication with login, signup,
     password reset, and persistent session management.

  2. Goals
     - Secure user registration and login
     - Password reset via email
     - Session persistence with JWT tokens
     - Role-based access (admin, user)

  3. User Stories
     - As a user, I can sign up with email and password
     - As a user, I can log in and receive a session token
     - As a user, I can reset my password via email link
     - As an admin, I can manage user roles

  4. Acceptance Criteria
     - All endpoints return proper HTTP status codes
     - Passwords hashed with bcrypt (min 12 rounds)
     - JWT tokens expire after 24 hours
     - Password reset links expire after 1 hour
     - 100% test coverage on auth endpoints

  Saved to: docs/prd-auth-system.md
```

### Step 3: UI Spec Generated / 步骤3：UI 规格说明生成

```
Workflows [design-agent] Generating UI Spec...

  UI Spec: Authentication Screens
  ================================
  Screen 1: Login Page (/login)
    Components: EmailInput, PasswordInput, LoginButton, ForgotPasswordLink
    Validation: email format, password min 8 chars
    States: idle, loading, error, success → redirect to /dashboard

  Screen 2: Signup Page (/signup)
    Components: EmailInput, PasswordInput, ConfirmPasswordInput, SignupButton
    Validation: email uniqueness (async), password match, strength meter
    States: idle, loading, error, success → redirect to /login

  Screen 3: Password Reset (/reset-password)
    Components: EmailInput, ResetButton (request), NewPasswordInput (confirm)
    Flow: request → email sent → click link → new password form

  Screen 4: Session Bar (global)
    Components: UserAvatar, UserName, LogoutButton
    Behavior: shows when authenticated, hides on /login and /signup

  Saved to: docs/ui-spec-auth-system.md
```

### Step 4: Design Doc with Architecture Decisions / 步骤4：设计文档与架构决策

```
Workflows [design-agent] Generating Design Doc...

  Design Doc: Authentication Architecture
  =========================================
  1. Architecture Decisions
     - JWT stored in httpOnly cookies (not localStorage) for XSS protection
     - Refresh token rotation: each refresh invalidates the old token
     - bcrypt with 12 rounds for password hashing
     - Rate limiting: 5 login attempts per minute per IP

  2. Data Models
     User: { id, email, password_hash, role, created_at, updated_at }
     Session: { id, user_id, refresh_token, expires_at, created_at }
     PasswordReset: { id, user_id, token, expires_at, used }

  3. API Contracts
     POST /api/auth/signup    → 201 { user }
     POST /api/auth/login     → 200 { token, refreshToken }
     POST /api/auth/logout    → 204
     POST /api/auth/refresh   → 200 { token, refreshToken }
     POST /api/auth/reset     → 202 { message }
     POST /api/auth/reset/:token → 200 { message }

  4. Security Considerations
     - CSRF protection via SameSite cookie attribute
     - Input sanitization on all endpoints
     - Timing-safe comparison for tokens

  Saved to: docs/design-doc-auth-system.md
```

### Step 5: Work Plan with 8 Ordered Tasks / 步骤5：工作计划包含 8 个有序任务

```
Workflows [design-agent] Generating Work Plan...

  Work Plan: 8 Tasks (ordered by dependency)
  ============================================
  Task 1: [Backend] Create User and Session database models
          Depends on: none
  Task 2: [Backend] Implement password hashing utilities
          Depends on: Task 1
  Task 3: [Backend] Build signup endpoint with validation
          Depends on: Tasks 1, 2
  Task 4: [Backend] Build login endpoint with JWT generation
          Depends on: Tasks 1, 2
  Task 5: [Backend] Build password reset (request + confirm)
          Depends on: Tasks 1, 2
  Task 6: [Backend] Implement auth middleware and RBAC
          Depends on: Task 4
  Task 7: [Frontend] Build Login, Signup, Reset UI components
          Depends on: Tasks 3, 4, 5 (needs API contracts)
  Task 8: [Testing] Write unit + integration tests for all endpoints
          Depends on: Tasks 3, 4, 5, 6

  Saved to: docs/work-plan-auth-system.md

All documents generated. Starting implementation...
```

### Step 6: Implementation Proceeds Task by Task / 步骤6：逐任务实现

```
Workflows [implementation-agent] Executing work plan...

  Task 1/8: Create database models ✓
    Created: models/user.py, models/session.py
  Task 2/8: Password hashing utilities ✓
    Created: utils/password.py
  Task 3/8: Signup endpoint ✓
    Created: routes/signup.py
  Task 4/8: Login endpoint ✓
    Created: routes/login.py
  Task 5/8: Password reset ✓
    Created: routes/reset.py
  Task 6/8: Auth middleware and RBAC ✓
    Created: middleware/auth.py, middleware/rbac.py
  Task 7/8: Frontend UI components ✓
    Created: components/LoginForm.tsx, SignupForm.tsx, ResetForm.tsx,
             SessionBar.tsx, AuthProvider.tsx
  Task 8/8: Test suite ✓
    Created: tests/test_auth.py, tests/test_ui_auth.tsx
```

### Step 7: Tests Run — One Fails, Auto-Fixed / 步骤7：测试运行 — 一个失败，自动修复

```
Workflows [quality-agent] Running test suite...

  pytest tests/test_auth.py
    ✓ test_signup_success
    ✓ test_signup_duplicate_email
    ✓ test_login_success
    ✓ test_login_wrong_password
    ✗ test_password_reset_expired_token    FAILED
      AssertionError: Expected 400, got 200
      Reset token was accepted after expiration time
    ✓ test_refresh_token_rotation
    ... (18 more tests pass)

  Result: 23 passed, 1 failed

Workflows [quality-agent] Auto-fixing failed test...
  Issue: Token expiration check missing in reset confirmation endpoint
  Fix: Added `if reset_request.expires_at < datetime.utcnow(): return 400`
  File modified: routes/reset.py (line 47)

  Re-running test suite...
    ✓ test_password_reset_expired_token    PASSED

  Result: 24 passed, 0 failed
```

### Step 8: Verification — Design Doc Matches Implementation / 步骤8：验证 — 设计文档与实现一致

```
Workflows [quality-agent] Verifying design doc ↔ implementation...

  Checking: API contracts match actual endpoints
    POST /api/auth/signup    → ✓ Implemented, returns 201
    POST /api/auth/login     → ✓ Implemented, returns 200
    POST /api/auth/logout    → ✓ Implemented, returns 204
    POST /api/auth/refresh   → ✓ Implemented, returns 200
    POST /api/auth/reset     → ✓ Implemented, returns 202
    POST /api/auth/reset/:token → ✓ Implemented, returns 200/400

  Checking: Data models match design
    User model:          ✓ All fields present
    Session model:       ✓ All fields present
    PasswordReset model: ✓ All fields present

  Checking: Security requirements
    httpOnly cookies:    ✓ Configured
    bcrypt 12 rounds:    ✓ Configured
    Rate limiting:       ✓ 5/min/IP
    CSRF protection:     ✓ SameSite=Strict

Workflows [quality-agent] VERIFICATION PASSED
  Design doc ↔ Implementation: 100% match
  All 24 tests passing
  All security requirements met

Pipeline complete. 15 files created, 4 documents generated.
```

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| `/plugin marketplace add` fails | Claude Code CLI outdated | Update CLI: `npm update -g @anthropic-ai/claude-code` / 更新 CLI |
| Workflow commands not available | Plugin not loaded after install | Restart Claude Code session: exit and run `claude` again / 重启 Claude Code 会话 |
| Complexity analyzer says "small" for a big task | Description too brief | Provide more detail in the task description: mention endpoints, screens, models / 在任务描述中提供更多细节 |
| PRD generation is empty | No codebase context | Ensure you run the command inside a project directory with source files / 确保在有源文件的项目目录中运行 |
| UI Spec skipped | No frontend detected | Add `--include-ui` flag or ensure frontend files exist in the project / 添加 `--include-ui` 标志或确保项目中有前端文件 |
| Design doc misses architecture details | Codebase analyzer cannot read some files | Check file permissions; ensure `.gitignore` is not hiding key files / 检查文件权限 |
| Implementation stalls on a task | Task dependency not met | Run `/workflow status` to see which task is blocked and why / 运行 `/workflow status` 查看阻塞原因 |
| Tests fail after auto-fix | Edge case not covered in design doc | Manually update the design doc, then re-run `/workflow verify` / 手动更新设计文档，然后重新运行 `/workflow verify` |
| Metronome plugin false alarm | Drift threshold too sensitive | Adjust in plugin settings: `/plugin config metronome --drift-threshold 15` / 调整插件设置 |

---

## Learn More / 了解更多

- GitHub: [github.com/shinpr/claude-code-workflows](https://github.com/shinpr/claude-code-workflows)
