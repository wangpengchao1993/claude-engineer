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

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置条件

Before installing Spec-Kit, you need:
在安装 Spec-Kit 之前，你需要：

1. **Node.js 18+**
   - Windows: Download from https://nodejs.org → run installer → restart terminal
   - macOS: `brew install node` or download from https://nodejs.org
   - Linux: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs`
   - Verify: `node --version` (should show v18.x or higher)

2. **Claude Code CLI**
   - Install: `npm install -g @anthropic-ai/claude-code`
   - Verify: `claude --version`
   - Login: `claude` (follow prompts to authenticate with your Anthropic API key)

3. **Git**
   - Windows: Download from https://git-scm.com
   - macOS: `xcode-select --install` or `brew install git`
   - Linux: `sudo apt install git`

### Step-by-Step Installation / 分步安装

Spec-Kit installs via the Claude Code plugin marketplace. The process is identical on all platforms.
Spec-Kit 通过 Claude Code 插件市场安装。所有平台的步骤完全相同。

#### All Platforms (Windows / macOS / Linux) / 所有平台

```bash
# Step 1: Open your project directory / 打开你的项目目录
cd /path/to/your/project

# Step 2: Start Claude Code / 启动 Claude Code
claude

# Step 3: Install from plugin marketplace / 从插件市场安装
# Inside Claude Code, type:
# 在 Claude Code 中输入：
/plugin marketplace add github/spec-kit

# Step 4: Verify installation / 验证安装
# Type any Spec-Kit command to confirm:
# 输入任意 Spec-Kit 命令确认：
/speckit.constitution
# If you see the constitution wizard, installation was successful!
# 如果看到宪法向导，安装成功！
```

#### Alternative: Manual Install / 替代方案：手动安装

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/github/spec-kit.git

# Copy plugin files to your project / 复制插件文件到你的项目
# macOS/Linux:
cp -r spec-kit/.claude/ /path/to/your/project/.claude/
# Windows (PowerShell):
Copy-Item -Recurse spec-kit\.claude\ C:\path\to\your\project\.claude\

# Start Claude Code / 启动 Claude Code
cd /path/to/your/project
claude
```

### What a Constitution File Looks Like in Detail / 宪法文件的详细样例

The Constitution is the most important file in Spec-Kit. Here is a comprehensive real-world example:
宪法是 Spec-Kit 中最重要的文件。以下是一个全面的真实世界示例：

```yaml
# .speckit/constitution.yaml
# This file defines the non-negotiable rules for your project
# 此文件定义项目中不可违背的规则

project:
  name: "E-Commerce API"
  description: "Backend API for an online marketplace"
  # 项目名称和描述

technologies:
  language: TypeScript 5.4
  runtime: Node.js 20 LTS
  framework: Fastify 4.x
  database: PostgreSQL 16
  cache: Redis 7
  orm: Drizzle ORM
  # 技术栈定义 -- 生成的代码必须使用这些技术

testing:
  required: true                    # Tests are mandatory / 测试是强制的
  minimum_coverage: 85%             # At least 85% code coverage / 至少 85% 代码覆盖率
  framework: vitest                 # Testing framework / 测试框架
  e2e_framework: playwright         # End-to-end testing / 端到端测试
  test_location: "__tests__/"       # Where tests live / 测试文件位置
  naming_convention: "*.test.ts"    # Test file naming / 测试文件命名

style:
  formatter: prettier
  linter: eslint (flat config)
  max_line_length: 100
  quotes: double
  semicolons: true
  indent: 2 spaces
  # 代码风格规则 -- 所有生成的代码必须遵守

api:
  style: RESTful
  versioning: URL path (/api/v1/)
  authentication: JWT with RS256
  documentation: OpenAPI 3.1
  error_format: RFC 7807 (Problem Details)
  # API 规范 -- 所有端点必须遵循

constraints:
  - All database queries must use parameterized statements (no string concatenation)
    所有数据库查询必须使用参数化语句（禁止字符串拼接）
  - Every endpoint must validate input with Zod schemas
    每个端点必须使用 Zod schema 验证输入
  - All errors must return RFC 7807 Problem Details format
    所有错误必须返回 RFC 7807 Problem Details 格式
  - No secrets in code -- all sensitive values from environment variables
    代码中禁止包含密钥 -- 所有敏感值从环境变量获取
  - Every public function must have JSDoc with @param and @returns
    每个公共函数必须有包含 @param 和 @returns 的 JSDoc
  - Database migrations must be reversible (up + down)
    数据库迁移必须可逆（up + down）
  - All timestamps must be UTC ISO 8601
    所有时间戳必须使用 UTC ISO 8601 格式

deployment:
  containerized: true (Docker)
  ci_cd: GitHub Actions
  environments: [dev, staging, production]
  # 部署约束
```

### Real-World Walkthrough / 真实操作演示

Here's a complete session building a "product catalog feature" using all 6 Spec-Kit phases:
以下是使用 Spec-Kit 全部 6 个阶段构建"产品目录功能"的完整会话：

```
# Step 1: Start Claude Code in your project
cd my-ecommerce-api
claude

# ═══════════════════════════════════════════════════════
# Phase 1: Constitution / 阶段 1：宪法
# ═══════════════════════════════════════════════════════

You:    /speckit.constitution

Claude: I'll help you define your project's constitution.
        我来帮你定义项目的宪法。

        I found an existing constitution at .speckit/constitution.yaml.
        发现已有宪法文件 .speckit/constitution.yaml。

        Current rules / 现有规则:
        - Language: TypeScript 5.4 + Fastify
        - Database: PostgreSQL 16 with Drizzle ORM
        - Testing: vitest, 85% minimum coverage
        - API: RESTful, JWT auth, OpenAPI docs

        Do you want to modify it or use as-is? (modify/use)
        要修改还是直接使用？（modify/use）

You:    use

# ═══════════════════════════════════════════════════════
# Phase 2: Specify / 阶段 2：规格说明
# ═══════════════════════════════════════════════════════

You:    /speckit.specify I need a product catalog with categories,
        search, and filtering

Claude: Creating specification based on your constitution...
        正在根据宪法创建规格说明...

        ## Product Catalog Specification / 产品目录规格说明

        ### Entities / 实体
        - Product: id, name, description, price, category_id, created_at
        - Category: id, name, slug, parent_id (supports nesting)
          产品和分类实体（支持嵌套分类）

        ### Endpoints / 端点
        - GET  /api/v1/products          -- List with pagination + filters
        - GET  /api/v1/products/:id       -- Get single product
        - POST /api/v1/products           -- Create (admin only)
        - PUT  /api/v1/products/:id       -- Update (admin only)
        - GET  /api/v1/products/search    -- Full-text search
        - GET  /api/v1/categories         -- List category tree
        - POST /api/v1/categories         -- Create (admin only)

        ### Non-functional / 非功能需求
        - Search response < 200ms (with Redis caching)
          搜索响应 < 200ms（使用 Redis 缓存）
        - Pagination: cursor-based, max 50 per page
          分页：基于游标，每页最多 50 条

        Saved to: .speckit/specs/product-catalog.md
        已保存至：.speckit/specs/product-catalog.md

# ═══════════════════════════════════════════════════════
# Phase 3: Clarify / 阶段 3：澄清歧义
# ═══════════════════════════════════════════════════════

You:    /speckit.clarify

Claude: I found 4 ambiguities in the specification:
        在规格说明中发现 4 处歧义：

        1. Should category nesting be unlimited depth or capped?
           分类嵌套是无限深度还是有上限？
        2. Should product search use PostgreSQL full-text or Elasticsearch?
           产品搜索使用 PostgreSQL 全文搜索还是 Elasticsearch？
        3. Should soft-delete or hard-delete be used for products?
           产品应使用软删除还是硬删除？
        4. Should product images be stored as URLs or uploaded files?
           产品图片存储为 URL 还是上传文件？

You:    1. Max 3 levels deep
        2. PostgreSQL full-text (keep it simple)
        3. Soft delete
        4. URLs only for now

Claude: ✅ Specification updated with clarifications.
           规格说明已更新。
        Saved to: .speckit/specs/product-catalog.md (v2)

# ═══════════════════════════════════════════════════════
# Phase 4: Plan / 阶段 4：规划
# ═══════════════════════════════════════════════════════

You:    /speckit.plan

Claude: Implementation plan (following constitution constraints):
        实施计划（遵循宪法约束）：

        Phase A: Database Layer / 数据库层
          - Create Drizzle schema for products + categories
          - Write reversible migrations (up + down, per constitution)
            编写可逆迁移（遵循宪法要求的 up + down）

        Phase B: Core CRUD / 核心 CRUD
          - Product CRUD with Zod validation (per constitution)
          - Category CRUD with nesting (max 3 levels)

        Phase C: Search & Filtering / 搜索和过滤
          - PostgreSQL full-text search setup
          - Redis caching layer for search results

        Phase D: Authorization / 授权
          - Admin-only guards for create/update/delete
          - JWT verification (RS256, per constitution)

        Saved to: .speckit/plans/product-catalog-plan.md

# ═══════════════════════════════════════════════════════
# Phase 5: Tasks / 阶段 5：任务拆分
# ═══════════════════════════════════════════════════════

You:    /speckit.tasks

Claude: Breaking plan into 8 concrete tasks:
        将计划拆分为 8 个具体任务：

        Task 1: [DB] Create Drizzle schema for Product + Category
        Task 2: [DB] Write migration files (up + down)
        Task 3: [API] Product CRUD endpoints + Zod schemas + tests
        Task 4: [API] Category CRUD with nesting validation + tests
        Task 5: [Search] PostgreSQL full-text search index + tests
        Task 6: [Search] Redis caching middleware + tests
        Task 7: [Auth] Admin authorization guards + tests
        Task 8: [Docs] OpenAPI documentation for all endpoints

        Each task includes acceptance criteria aligned with the constitution.
        每个任务都包含与宪法对齐的验收标准。

        Saved to: .speckit/tasks/product-catalog-tasks.md
        Export to GitHub Issues? (yes/no)
        导出为 GitHub Issues？（是/否）

You:    no

# ═══════════════════════════════════════════════════════
# Phase 6: Implement / 阶段 6：执行实现
# ═══════════════════════════════════════════════════════

You:    /speckit.implement

Claude: Starting implementation of Task 1 of 8...
        开始实现第 1 个任务（共 8 个）...

        [Task 1] Creating Drizzle schema...
        ✅ src/db/schema/product.ts created
        ✅ src/db/schema/category.ts created
        ✅ All parameterized queries (per constitution)
           所有查询已参数化（遵循宪法）
        ✅ Timestamps in UTC ISO 8601 (per constitution)
           时间戳使用 UTC ISO 8601（遵循宪法）

        [Task 2] Writing migrations...
        ✅ migrations/001_create_products.ts (up + down)
        ✅ migrations/002_create_categories.ts (up + down)
           迁移文件可逆（遵循宪法）

        [Task 3] Product CRUD endpoints...
        ✅ src/routes/products.ts created
        ✅ src/schemas/product.zod.ts created (per constitution)
        ✅ __tests__/products.test.ts -- 12 tests passing
           12 个测试通过

        ... (Tasks 4-8 follow the same pattern)
        ...（任务 4-8 遵循相同模式）

        ══════════════════════════════════════
        Final Summary / 最终摘要:
        ✅ 8/8 tasks completed / 8 个任务全部完成
        ✅ 47 tests passing / 47 个测试通过
        ✅ 91% code coverage (above 85% minimum) / 91% 覆盖率
        ✅ All constitution constraints satisfied / 所有宪法约束已满足
        ✅ OpenAPI docs generated / OpenAPI 文档已生成
```

### Troubleshooting / 常见问题

| Problem / 问题 | Solution / 解决方案 |
|----------------|---------------------|
| `/speckit.constitution` not recognized / 命令未识别 | Re-install: `/plugin marketplace add github/spec-kit`. Restart Claude Code / 重新安装并重启 Claude Code |
| "No constitution found" error / "未找到宪法"错误 | Run `/speckit.constitution` first to create one. It must exist before other commands / 先运行 `/speckit.constitution` 创建宪法，其他命令依赖它 |
| Spec-Kit skips clarify phase / 跳过澄清阶段 | Explicitly run `/speckit.clarify` -- it won't auto-trigger / 明确运行 `/speckit.clarify`，它不会自动触发 |
| Constitution file not found after manual install / 手动安装后找不到宪法文件 | Ensure `.speckit/` directory is in your project root (not `.claude/`) / 确保 `.speckit/` 目录在项目根目录中 |
| Tasks don't match the plan / 任务与计划不匹配 | Re-run `/speckit.plan` then `/speckit.tasks` -- tasks are generated from the latest plan / 重新运行 `/speckit.plan` 再运行 `/speckit.tasks` |
| Plugin install fails on Windows / Windows 上插件安装失败 | Use PowerShell (not CMD). Ensure Claude Code is updated to the latest version / 使用 PowerShell，确保 Claude Code 是最新版本 |
| Implementation violates constitution rules / 实现违反宪法规则 | Run `/speckit.analyze` to check compliance. Fix violations, then re-run `/speckit.implement` / 运行 `/speckit.analyze` 检查合规性，修复后重新实现 |

---

*Spec-Kit enforces the discipline that turns AI from a guessing machine into a
precision tool. Define first, build second.*

*Spec-Kit 强制执行纪律, 将 AI 从猜测机器变成精密工具。先定义, 再构建。*
