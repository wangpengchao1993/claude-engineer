# GStack -- Garry Tan's Virtual Engineering Team

# GStack -- YC CEO 的虚拟工程团队

> **~83k stars** | By **Garry Tan** (Y Combinator CEO) | MIT License
>
> GitHub: [github.com/garrytan/gstack](https://github.com/garrytan/gstack)

---

## What is GStack? / 什么是 GStack？

GStack turns Claude Code into a **complete engineering team** with specialized roles.
Think of it as having a CTO, designer, eng manager, QA lead, security officer,
and release engineer -- all AI, all opinionated, all working for you.

GStack 把 Claude Code 变成一个**完整的工程团队**，每个角色各司其职。
就像同时拥有 CTO、设计师、工程经理、QA 负责人、安全官和发布工程师——全部由 AI 担任。

Garry Tan averaged **10,000 lines of code** and **100 pull requests per week** using this setup.
After months of personal use, he open-sourced it in March 2026.

Garry Tan 使用这套系统平均每周产出 **10,000 行代码**和 **100 个 PR**。
经过数月的个人使用后，于 2026 年 3 月开源。

---

## The Virtual Team / 虚拟团队

GStack assigns Claude Code **strong, opinionated roles**. Each role has firm beliefs
about what "good" looks like -- that's the secret sauce.

GStack 为 Claude Code 分配了**有主见的角色**。每个角色对"什么是好的"都有坚定的看法——这是秘诀所在。

| Role / 角色 | What They Do / 职责 | Key Trait / 关键特质 |
|---|---|---|
| **CEO** | Rethinks the product -- is this worth building? / 重新审视产品——值得做吗？ | Vision-driven / 愿景驱动 |
| **Eng Manager** | Locks architecture, defines constraints / 锁定架构、定义约束 | Consistency-obsessed / 一致性强迫症 |
| **Designer** | Catches "AI slop" -- generic, lifeless UI / 捕捉"AI 水货"——模板化、无生气的界面 | Taste-driven / 审美驱动 |
| **Code Reviewer** | Finds production bugs before they ship / 在上线前发现生产级 Bug | Paranoid / 偏执型审查 |
| **QA Lead** | Opens a real browser, runs test scenarios / 打开真实浏览器、运行测试场景 | Hands-on testing / 实操测试 |
| **Security Officer** | Runs OWASP + STRIDE threat audits / 执行 OWASP + STRIDE 威胁审计 | Zero-trust mindset / 零信任思维 |
| **Release Engineer** | Ships the PR, handles changelog / 发布 PR、维护变更日志 | Ship-it mentality / 发布至上 |

---

## 23+ Slash Commands / 23+ 斜杠命令

GStack provides 23 opinionated slash commands (Claude Code "skills") that map to
the roles above. Some highlights:

GStack 提供 23 个有主见的斜杠命令（Claude Code "技能"），对应上面的角色。部分命令如下：

```
/ceo-review        -- CEO perspective: should we build this?
                      CEO 视角：我们该不该做这个？

/arch-lock         -- Lock down architecture decisions
                      锁定架构决策

/design-review     -- Check UI for AI slop and generic patterns
                      检查界面是否有 AI 水货和模板化问题

/code-review       -- Deep review for production bugs
                      深度审查生产级 Bug

/qa-browser        -- Launch real browser testing
                      启动真实浏览器测试

/security-audit    -- OWASP + STRIDE threat modeling
                      OWASP + STRIDE 威胁建模

/ship-pr           -- Create and ship the pull request
                      创建并发布 PR

/standup           -- Daily standup summary
                      每日站会摘要

/retro             -- Sprint retrospective
                      迭代回顾
```

Each command embeds domain expertise. `/design-review` knows what AI slop looks like.
`/security-audit` runs through real OWASP checklists. These are not generic prompts.

每个命令都内嵌了领域专业知识。`/design-review` 知道 AI 水货长什么样。
`/security-audit` 会遍历真实的 OWASP 检查清单。这些不是泛泛的提示词。

---

## Installation / 安装

Add GStack's commands to your project's `.claude/` directory:

将 GStack 的命令添加到项目的 `.claude/` 目录：

```bash
# Clone the repo / 克隆仓库
git clone https://github.com/garrytan/gstack.git

# Copy commands into your project / 将命令复制到你的项目
cp -r gstack/commands/ your-project/.claude/commands/
```

That's it. Claude Code will automatically discover the slash commands.

就这样。Claude Code 会自动发现这些斜杠命令。

---

## Key Insight: Opinionated Roles / 核心理念：有主见的角色

The word **opinionated** is central to GStack. Each role doesn't just "help" --
it has **strong opinions** about what good looks like:

**有主见**是 GStack 的核心理念。每个角色不只是"帮忙"——它对什么是好的有**强烈的看法**：

- The **Designer** will reject bland, template-driven UI and push for personality.
  **设计师**会拒绝乏味的模板化 UI，并要求注入个性。

- The **Security Officer** assumes everything is compromised until proven otherwise.
  **安全官**假设一切都已被攻破，除非证明安全。

- The **Code Reviewer** looks for the bug that will wake you up at 3 AM.
  **代码审查员**寻找那些会在凌晨 3 点把你叫醒的 Bug。

- The **Eng Manager** won't let you introduce a new pattern that conflicts with existing ones.
  **工程经理**不会让你引入与现有模式冲突的新模式。

This opinionated approach is what makes GStack effective. Generic advice is cheap;
strong, specific feedback is valuable.

这种有主见的方法正是 GStack 有效的原因。泛泛的建议廉价；强烈、具体的反馈才有价值。

---

## GStack vs Superpowers / GStack 与 Superpowers 对比

Both are popular Claude Code frameworks, but they take different approaches:

两者都是流行的 Claude Code 框架，但采用不同的策略：

| Aspect / 方面 | GStack | Superpowers |
|---|---|---|
| **Mental model / 思维模型** | Role-based team / 基于角色的团队 | Phase-based workflow / 基于阶段的流程 |
| **Core idea / 核心理念** | Each command = a team member / 每个命令=一个团队成员 | Each phase = a development stage / 每个阶段=一个开发环节 |
| **Strength / 优势** | Deep domain expertise per role / 每个角色深度领域专长 | Structured progression / 结构化推进 |
| **Best for / 适合** | Solo devs who want a team / 想要团队的独立开发者 | Teams wanting process / 想要流程的团队 |
| **Philosophy / 哲学** | Opinionated specialists / 有主见的专家 | Guided steps / 引导式步骤 |

They are complementary. Some developers use both.

两者是互补的。有些开发者同时使用。

---

## Learn More / 了解更多

- **GitHub**: [github.com/garrytan/gstack](https://github.com/garrytan/gstack)
- **Author**: Garry Tan -- CEO of Y Combinator
- **License**: MIT
- **Stars**: ~83,000

---

---

## Complete Setup Guide / 完整安装指南

### Prerequisites / 前置要求

Before installing GStack, ensure you have the following:

安装 GStack 之前，请确保已安装以下工具：

| Requirement / 要求 | Minimum Version / 最低版本 | Purpose / 用途 |
|---|---|---|
| **Node.js** | 18+ | Required for Claude Code CLI / Claude Code CLI 运行所需 |
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

GStack is installed by copying slash command files into your project's `.claude/commands/` directory.

GStack 通过将斜杠命令文件复制到项目的 `.claude/commands/` 目录来安装。

```bash
# 1. Clone the GStack repository / 克隆 GStack 仓库
git clone https://github.com/garrytan/gstack.git

# 2. Navigate to your project / 进入你的项目目录
cd your-project

# 3. Create the Claude commands directory if it doesn't exist
# 如果不存在，创建 Claude 命令目录
mkdir -p .claude/commands

# 4. Copy all GStack commands / 复制所有 GStack 命令
cp -r /path/to/gstack/commands/* .claude/commands/

# 5. Start Claude Code / 启动 Claude Code
claude
```

**One-liner (all platforms) / 一行命令（所有平台）：**

```bash
git clone https://github.com/garrytan/gstack.git /tmp/gstack && mkdir -p .claude/commands && cp -r /tmp/gstack/commands/* .claude/commands/
```

**Windows PowerShell equivalent / Windows PowerShell 等价命令：**

```powershell
git clone https://github.com/garrytan/gstack.git $env:TEMP\gstack; New-Item -ItemType Directory -Force -Path .claude\commands; Copy-Item -Recurse "$env:TEMP\gstack\commands\*" .claude\commands\
```

### Verification / 验证安装

```bash
# Verify Node.js / 验证 Node.js
node --version
# Expected: v18.x.x or higher / 预期: v18.x.x 或更高

# Verify Claude Code is available / 验证 Claude Code 可用
claude --version

# Verify commands were copied / 验证命令已复制
ls .claude/commands/
# Expected: ceo-review.md, arch-lock.md, design-review.md,
#           code-review.md, qa-browser.md, security-audit.md,
#           ship-pr.md, standup.md, retro.md, and more
# 预期：上述命令文件

# Inside Claude Code, verify commands are discovered
# 在 Claude Code 内验证命令已被发现
# Type: / and press Tab to see all available slash commands
# 输入: / 然后按 Tab 查看所有可用斜杠命令
```

---

## Real-World Walkthrough / 真实操作演示

Below is a complete GStack session building a user dashboard feature for a SaaS app. This demonstrates how each team member contributes their specialized expertise to produce production-ready code.

以下是使用 GStack 为 SaaS 应用构建用户仪表板功能的完整会话。演示每个团队成员如何贡献其专业知识来产出生产级代码。

### Step 1: CEO Review -- Should we build this? / 第一步：CEO 审查——该不该做？

```
$ cd saas-app
$ claude

You: I want to add a real-time analytics dashboard showing user
     engagement metrics, revenue charts, and team activity.

You: /ceo-review

Claude (as CEO):
  🎯 CEO Review: Real-time Analytics Dashboard

  VERDICT: GO -- with scope reduction

  Strategic Assessment:
  ✅ High value: Dashboards are the #1 requested feature in user surveys
  ✅ Retention driver: Users who view analytics have 3x higher retention
  ⚠️ Scope concern: "Real-time" adds significant infrastructure cost

  Recommendation:
  - Build the dashboard with NEAR-real-time (5-minute refresh)
    instead of true real-time (WebSocket). This covers 95% of the
    value at 20% of the infrastructure cost.
  - Phase 1: Engagement metrics + revenue charts
  - Phase 2: Team activity (defer to next sprint)

  Proceed with Phase 1 scope? This is a high-leverage feature.
```

### Step 2: Architecture Lock -- Define constraints / 第二步：架构锁定——定义约束

```
You: /arch-lock

Claude (as Eng Manager):
  🔒 Architecture Lock: Dashboard Feature

  CONSTRAINTS (violations will be flagged in code review):

  1. Data layer: Use existing PostgreSQL -- NO new databases.
     We already have pg_cron for scheduled jobs. Use materialized
     views refreshed every 5 minutes for dashboard queries.

  2. API pattern: Follow existing REST conventions in src/api/.
     New routes under /api/v1/analytics/*.
     Return shape: { data: T, meta: { refreshedAt: string } }

  3. Frontend: Use existing Chart.js library (already in bundle).
     Do NOT add a new charting library. Dashboard goes in
     src/components/dashboard/ following existing component patterns.

  4. Auth: Dashboard requires 'analytics:read' permission.
     Use existing RBAC middleware. No new auth patterns.

  5. Testing: Minimum 80% coverage on new service layer code.

  These constraints are now locked. /code-review will enforce them.
```

### Step 3: Design Review -- Catch AI slop / 第三步：设计审查——发现 AI 水货

```
You: [after building initial UI]

You: /design-review

Claude (as Designer):
  🎨 Design Review: Dashboard UI

  AI SLOP DETECTED -- 3 issues:

  ❌ Issue 1: Generic card layout
     You're using the default "3 cards in a row" pattern that every
     AI generates. Your app uses a distinctive sidebar-metric style
     everywhere else. Match the existing pattern.

  ❌ Issue 2: Default Chart.js colors
     The charts use Chart.js default blue/red/green. Your app's
     design system uses specific brand colors defined in
     tailwind.config.ts under theme.colors.chart.*.

  ❌ Issue 3: No empty state
     When there's no data yet, the dashboard shows a blank white
     screen. Design an empty state with an illustration and
     "Start tracking" CTA -- consistent with your onboarding flow.

  Required changes:
  1. Replace card grid with sidebar-metric layout from DesignSystem.md
  2. Use theme.colors.chart.* for all Chart.js datasets
  3. Add empty state component matching src/components/EmptyState.tsx

  Fix these before proceeding to code review.
```

### Step 4: Code Review -- Find production bugs / 第四步：代码审查——发现生产级 Bug

```
You: [after fixing design issues]

You: /code-review

Claude (as Code Reviewer):
  🔍 Code Review: Dashboard Implementation

  BUGS FOUND -- 2 critical, 1 warning:

  🔴 CRITICAL: SQL injection in date range filter
     File: src/api/analytics/revenue.ts:42
     You're interpolating user-provided startDate directly into
     the SQL query. Use parameterized queries via Drizzle.

  🔴 CRITICAL: Missing auth middleware
     File: src/api/analytics/index.ts:8
     The /api/v1/analytics/engagement route has no auth middleware.
     All other routes in the file use requirePermission('analytics:read').
     This is an exposed endpoint.

  🟡 WARNING: Architecture violation
     File: src/api/analytics/revenue.ts:15
     You're importing from src/components/ in an API route.
     This violates the existing layered architecture.
     Move shared types to src/types/analytics.ts.

  Blocking merge until critical issues are resolved.
```

### Step 5: QA Browser Testing / 第五步：浏览器 QA 测试

```
You: [after fixing bugs]

You: /qa-browser

Claude (as QA Lead):
  🧪 Browser Testing: Dashboard Feature

  Launching Playwright browser...

  Test Scenarios:
  ✅ Dashboard loads within 2 seconds on desktop (1280x720)
  ✅ Charts render correctly with sample data
  ✅ Empty state displays when no data exists
  ✅ Date range picker filters data correctly
  ✅ Dashboard is responsive at mobile breakpoints (375px, 768px)
  ✅ Unauthorized user gets 403, not a blank page
  ⚠️ Charts overlap sidebar at 1024px tablet breakpoint
  ✅ Data refreshes every 5 minutes without page reload

  Results: 7/8 passing, 1 layout issue at tablet breakpoint.

  Screenshot saved: .qa/screenshots/tablet-overlap.png
  Fix the 1024px breakpoint, then we can ship.
```

### Step 6: Security Audit / 第六步：安全审计

```
You: [after fixing tablet layout]

You: /security-audit

Claude (as Security Officer):
  🛡️ Security Audit: Dashboard Feature

  OWASP Top 10 Check:
  ✅ A01 Broken Access Control -- RBAC enforced on all routes
  ✅ A02 Cryptographic Failures -- No sensitive data in responses
  ✅ A03 Injection -- Parameterized queries (fixed from code review)
  ✅ A04 Insecure Design -- Rate limiting on analytics endpoints
  ✅ A05 Security Misconfiguration -- CORS properly scoped
  ✅ A06 Vulnerable Components -- No new dependencies added
  ✅ A07 Auth Failures -- JWT validation on all routes
  ✅ A08 Data Integrity -- Response checksums verified
  ⚠️ A09 Logging -- Analytics queries not logged for audit trail
  ✅ A10 SSRF -- No external URL fetching

  STRIDE Threat Model:
  ✅ Spoofing: JWT required
  ✅ Tampering: Parameterized queries prevent SQL manipulation
  ✅ Repudiation: ⚠️ Add audit logging for analytics access
  ✅ Information Disclosure: No PII in analytics responses
  ✅ Denial of Service: Rate limiting in place
  ✅ Elevation of Privilege: RBAC enforced

  Result: PASS with 1 recommendation
  Add audit logging for analytics endpoint access before shipping.
```

### Step 7: Ship the PR / 第七步：发布 PR

```
You: [after adding audit logging]

You: /ship-pr

Claude (as Release Engineer):
  🚀 Shipping: Dashboard Feature

  Pre-flight checks:
  ✅ All tests pass (42 new tests, 100% of new code covered)
  ✅ TypeScript compiles cleanly
  ✅ No lint errors
  ✅ Design review: APPROVED
  ✅ Code review: APPROVED
  ✅ Security audit: PASSED
  ✅ QA browser testing: PASSED

  Creating pull request...

  PR #287: Add near-real-time analytics dashboard
  ├── 18 files changed, +1,247 -23
  ├── Linked to: FEAT-1042
  ├── Reviewers: auto-assigned based on CODEOWNERS
  ├── Labels: feature, analytics
  └── URL: https://github.com/your-org/saas-app/pull/287

  Changelog entry added to CHANGELOG.md.
  Ready for human review and merge.
```

### Why Every Step Mattered / 为什么每一步都很重要

Without GStack's opinionated reviewers, this feature would have shipped with:
- SQL injection vulnerability (caught by `/code-review`)
- Missing authentication on an endpoint (caught by `/code-review`)
- Generic AI-generated UI that doesn't match the app (caught by `/design-review`)
- Tablet layout breakage (caught by `/qa-browser`)
- Missing audit trail (caught by `/security-audit`)
- Over-scoped real-time requirement (caught by `/ceo-review`)

没有 GStack 的有主见审查员，这个功能上线时会带着：SQL 注入漏洞、缺失的端点认证、与应用风格不符的 AI 模板 UI、平板布局错位、缺失的审计日志、以及过度设计的实时需求。

---

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Solution / 解决方案 |
|---|---|---|
| Slash commands not showing in Claude Code | Commands not in `.claude/commands/` directory / 命令不在 `.claude/commands/` 目录 | Verify: `ls .claude/commands/` -- files must be `.md` format / 验证文件存在且为 `.md` 格式 |
| `git clone` fails for GStack repo | Network issue or repo URL changed / 网络问题或仓库地址变更 | Check [github.com/garrytan/gstack](https://github.com/garrytan/gstack) for the current URL / 访问 GitHub 确认当前地址 |
| `/qa-browser` cannot launch browser | Playwright or browser not installed / Playwright 或浏览器未安装 | Run `npx playwright install` to install browsers / 运行 `npx playwright install` 安装浏览器 |
| `/security-audit` produces shallow results | Not enough code context provided / 未提供足够的代码上下文 | Specify the feature scope: `/security-audit the new analytics dashboard in src/api/analytics/` / 指定功能范围 |
| Commands return generic responses | `.claude/CLAUDE.md` not configured / CLAUDE.md 未配置 | Ensure your project has a CLAUDE.md with project-specific context / 确保项目有包含项目上下文的 CLAUDE.md |
| `claude` command not found | Claude Code CLI not installed globally / Claude Code CLI 未全局安装 | Run `npm install -g @anthropic-ai/claude-code` / 运行全局安装命令 |
| `/design-review` misses project style | No design system documentation in project / 项目中无设计系统文档 | Add a DesignSystem.md or reference your Tailwind config in CLAUDE.md / 添加设计系统文档或在 CLAUDE.md 中引用 Tailwind 配置 |
| `/ship-pr` fails to create PR | Not on a feature branch or no remote configured / 不在功能分支或无远程仓库 | Create a branch first: `git checkout -b feat/your-feature` and push / 先创建分支并推送 |

---

*GStack shows that the best AI coding isn't about one mega-prompt --
it's about assembling a team of specialists, each with strong opinions.*

*GStack 证明了最好的 AI 编程不是靠一个超级提示词——而是组建一支专家团队，每位专家都有强烈的主见。*
