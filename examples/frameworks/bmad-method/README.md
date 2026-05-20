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

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置要求

Before installing BMAD-METHOD, ensure you have the following:

安装 BMAD-METHOD 之前，请确保已安装以下工具：

| Requirement / 要求 | Minimum Version / 最低版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Runtime for BMAD CLI / BMAD CLI 运行时 |
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

**Option A: NPX install (recommended, all platforms) / NPX 安装（推荐，所有平台）**

```bash
# 1. Navigate to your project / 进入你的项目目录
cd your-project

# 2. Initialize a git repo if needed / 如需要，初始化 git 仓库
git init

# 3. Run the BMAD installer / 运行 BMAD 安装器
npx bmad-method@next install

# 4. Start Claude Code / 启动 Claude Code
claude
```

**Option B: Claude Code Native Skills / Claude Code 原生技能方式**

```bash
# 1. Clone the BMAD skills repo / 克隆 BMAD 技能仓库
git clone https://github.com/bmad-code-org/BMAD-METHOD.git

# 2. Copy skill files to your project / 将技能文件复制到你的项目
cp -r BMAD-METHOD/skills/ your-project/.claude/commands/

# 3. Navigate to your project / 进入项目目录
cd your-project

# 4. Start Claude Code -- agents are now available as slash commands
# 启动 Claude Code -- 智能体现在可用作斜杠命令
claude
```

### Verification / 验证安装

```bash
# Verify Node.js / 验证 Node.js
node --version
# Expected: v18.x.x or higher / 预期: v18.x.x 或更高

# Verify Claude Code is available / 验证 Claude Code 可用
claude --version

# Verify BMAD files were created / 验证 BMAD 文件已创建
ls .bmad/ 2>/dev/null || ls .claude/commands/ 2>/dev/null
# Expected: agent configuration files, templates
# 预期：智能体配置文件、模板

# Inside Claude Code, test agent availability / 在 Claude Code 内测试智能体可用性
# Type: /bmad- and press Tab to see available commands
# 输入: /bmad- 然后按 Tab 查看可用命令
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete BMAD session building an e-commerce API. This demonstrates a full agile sprint with AI agents playing each role, then a second sprint incorporating feedback.

以下是使用 BMAD 构建电商 API 的完整会话。演示由 AI 智能体扮演每个角色的完整敏捷冲刺，以及整合反馈的第二次冲刺。

### Sprint 1: Build the Core / 冲刺 1：构建核心

#### Phase 1: Product Manager gathers requirements / 阶段 1：产品经理收集需求

```
$ cd ecommerce-api
$ npx bmad-method@next install

> BMAD-METHOD installed successfully.
> Agent configurations created in .bmad/
> CLAUDE.md updated with BMAD directives.
> Start Claude Code and invoke the PM agent to begin.

$ claude

You: I want to build an e-commerce REST API with product catalog,
     shopping cart, and checkout with Stripe payments.

You: /bmad-pm

Claude (as Product Manager):
  🎯 Product Manager Agent activated.

  I'll gather requirements and produce a PRD with user stories.

  Based on your description, here is the draft PRD:

  ── Product Requirements Document ──────────────────
  Product: E-Commerce REST API
  Target users: Frontend developers consuming the API
  Core domains: Products, Cart, Checkout, Payments

  User Stories:
  US-1: As a shopper, I can browse products with pagination and filters
  US-2: As a shopper, I can add/remove items from my cart
  US-3: As a shopper, I can checkout and pay via Stripe
  US-4: As an admin, I can create/update/delete products
  US-5: As a developer, I get clear error messages and API docs

  Acceptance Criteria defined for each story.
  PRD saved to: .bmad/artifacts/prd.md

  Questions for you:
  1. Do you need user accounts or guest checkout only?
  2. Any specific product attributes beyond name/price/description?
  3. Target deployment: serverless, container, or traditional server?
  ─────────────────────────────────────────────────────

You: User accounts with JWT auth. Products have images and categories.
     Deploy with Docker containers.

Claude (as PM):
  PRD updated with:
  - US-6: User registration and JWT authentication
  - US-7: Product image upload and category filtering
  - Deployment target: Docker containers
  PRD finalized. Ready for Architect.
```

#### Phase 2: Architect designs the system / 阶段 2：架构师设计系统

```
You: /bmad-architect

Claude (as Architect):
  🏗️ Architect Agent activated.
  Reading PRD from .bmad/artifacts/prd.md...

  ── Architecture Decision Record ───────────────────
  Tech Stack:
  - Runtime: Node.js 20 + TypeScript
  - Framework: Fastify (performance over Express)
  - Database: PostgreSQL 16 with Drizzle ORM
  - Auth: JWT with refresh tokens
  - Payments: Stripe SDK
  - Storage: S3-compatible for product images
  - Containerization: Docker + docker-compose

  System Design:
  ┌─────────────┐     ┌──────────────┐     ┌──────────┐
  │  API Layer  │────▶│ Service Layer│────▶│   DB     │
  │  (Fastify)  │     │  (Business)  │     │ (Postgres)│
  └─────────────┘     └──────────────┘     └──────────┘
         │                    │
         ▼                    ▼
  ┌─────────────┐     ┌──────────────┐
  │  Auth (JWT) │     │ Stripe API   │
  └─────────────┘     └──────────────┘

  API Routes:
  POST   /auth/register, /auth/login, /auth/refresh
  GET    /products, /products/:id
  POST   /products (admin)
  GET    /cart
  POST   /cart/items, DELETE /cart/items/:id
  POST   /checkout

  Architecture doc saved to: .bmad/artifacts/architecture.md
  ─────────────────────────────────────────────────────
```

#### Phase 3: Developer implements / 阶段 3：开发者实现

```
You: /bmad-developer

Claude (as Developer):
  👨‍💻 Developer Agent activated.
  Reading architecture from .bmad/artifacts/architecture.md...
  Reading PRD from .bmad/artifacts/prd.md...

  Implementing US-1 through US-7...

  ✅ Created project structure:
     src/routes/auth.ts       - Registration, login, refresh
     src/routes/products.ts   - CRUD + image upload
     src/routes/cart.ts       - Cart management
     src/routes/checkout.ts   - Stripe checkout flow
     src/services/           - Business logic layer
     src/db/schema.ts        - Drizzle ORM schema
     src/db/migrations/      - Database migrations
     src/middleware/auth.ts   - JWT middleware
     docker-compose.yml      - PostgreSQL + API containers
     Dockerfile              - Multi-stage build

  ✅ All routes implemented per architecture spec
  ✅ TypeScript compiles cleanly
  ✅ Docker containers build successfully
```

#### Phase 4: QA tests / 阶段 4：QA 测试

```
You: /bmad-qa

Claude (as QA Engineer):
  🧪 QA Agent activated.
  Reading user stories and acceptance criteria...

  Running test suite:
  ✅ Auth: Register new user              PASS
  ✅ Auth: Login returns JWT              PASS
  ✅ Auth: Refresh token works            PASS
  ✅ Auth: Invalid token rejected         PASS
  ✅ Products: List with pagination       PASS
  ✅ Products: Filter by category         PASS
  ✅ Products: Admin CRUD                 PASS
  ⚠️ Cart: Add item with quantity 0      FAIL - should reject, got 200
  ✅ Cart: Remove item                    PASS
  ✅ Checkout: Stripe payment intent      PASS
  ⚠️ Checkout: Expired cart checkout     FAIL - no cart expiry implemented

  Results: 9/11 passing, 2 bugs found
  Bug reports saved to: .bmad/artifacts/bugs-sprint1.md

  Bug 1: Cart accepts zero-quantity items (missing validation)
  Bug 2: No cart expiry -- stale carts can checkout indefinitely
```

### Sprint 2: Fix Bugs + Add Features / 冲刺 2：修复 Bug + 增加功能

```
You: Fix the two bugs from QA and add product search.

You: /bmad-pm

Claude (as PM):
  Sprint 2 scope:
  - BUG-1: Add quantity validation (min: 1) to cart
  - BUG-2: Add 24-hour cart expiry with cleanup job
  - US-8: Full-text product search with relevance ranking
  PRD updated.

You: /bmad-developer

Claude (as Developer):
  Reading updated PRD and bug reports...
  ✅ Fixed: Cart quantity validation (rejects qty <= 0)
  ✅ Fixed: Cart expiry (24h TTL + pg_cron cleanup)
  ✅ Added: GET /products/search?q= with pg_trgm full-text search

You: /bmad-qa

Claude (as QA):
  Re-running full suite + new tests:
  ✅ 11/11 previous tests PASS (including 2 bug fixes)
  ✅ Search: Returns relevant products               PASS
  ✅ Search: Empty query returns 400                  PASS
  ✅ Cart: Expired cart returns 410 Gone              PASS

  Results: 14/14 passing. All acceptance criteria met.
  Sprint 2: COMPLETE
```

This iterative pattern -- PM defines, Architect designs, Developer builds, QA catches issues, then repeat -- is the core strength of BMAD. Each agent has specialized knowledge and perspective that catches what others miss.

这种迭代模式——PM 定义、架构师设计、开发者构建、QA 发现问题、然后重复——是 BMAD 的核心优势。每个智能体都有专业知识和视角，能发现其他智能体遗漏的问题。

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| `npx bmad-method@next install` fails | npm registry unreachable or Node.js too old / npm 注册表不可达或 Node.js 版本太旧 | Check internet connection; verify `node --version` is 18+ / 检查网络连接；验证 Node.js 版本 >= 18 |
| Agent slash commands not visible | Skills not in `.claude/commands/` directory / 技能不在 `.claude/commands/` 目录 | Verify files exist: `ls .claude/commands/` or re-run installer / 验证文件存在，或重新运行安装器 |
| Agent produces generic output | PRD or architecture doc missing / PRD 或架构文档缺失 | Run agents in order: PM first, then Architect, then Developer / 按顺序运行：先 PM，再架构师，再开发者 |
| `claude` command not found | Claude Code CLI not installed globally / Claude Code CLI 未全局安装 | Run `npm install -g @anthropic-ai/claude-code` / 运行全局安装命令 |
| Agent loses context between phases | Artifact files not saved correctly / 产出文件未正确保存 | Check `.bmad/artifacts/` directory for PRD and architecture docs / 检查 `.bmad/artifacts/` 目录 |
| Permission error during install on Linux | npm global install requires elevated privileges / npm 全局安装需要提升权限 | Use `sudo npm install -g` or configure npm prefix: `npm config set prefix ~/.npm-global` / 使用 sudo 或配置 npm 前缀 |
| QA agent cannot run tests | Test dependencies not installed / 测试依赖未安装 | Run `npm install` to ensure all dev dependencies are present / 运行 `npm install` 确保开发依赖已安装 |
| Codebase Flattener produces empty output | Running from wrong directory / 从错误目录运行 | Ensure you are in the project root with source files / 确保在包含源文件的项目根目录 |

---

*This example is part of the Claude Engineer frameworks collection.*

*本示例是 Claude Engineer 框架合集的一部分。*
