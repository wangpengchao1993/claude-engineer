# AI Coding Workflow Frameworks
# AI 编码工作流框架

> **English** | [中文](#中文版导航)

Transform AI coding from "chatting with a bot" into disciplined engineering: requirements → design → implement → review → ship.

---

## Table of Contents

- [What is a Harness?](#what-is-a-harness--什么是-harness)
- [Quick Comparison](#quick-comparison--快速对比)
- [Which Framework Should I Use?](#which-framework-should-i-use--我该用哪个框架)
- [Demo Config Checklist](#demo-config-checklist--配置清单)
- [Detailed Feature Matrix](#detailed-feature-matrix--详细功能矩阵)
- [Framework Profiles](#framework-profiles--框架详情)
- [Learning Path](#learning-path--学习路径)
- [中文版导航](#中文版导航)

---

## What is a Harness? / 什么是 Harness?

```
Without Harness:                          With Harness:
没有 Harness：                              有 Harness：

"Build me a login page"                   Idea → Spec → Plan → TDD → Code → Review → Ship
     ↓                                    想法 → 规格 → 计划 → TDD → 代码 → 审查 → 交付
AI writes code immediately                     ↓
     ↓                                    Each step verified before next
Maybe works, maybe not                    每一步都在下一步之前验证
Maybe forgot half the requirements        No requirements forgotten
也许忘了一半需求                            不会遗漏需求
```

A **harness framework** sits on top of Claude Code and enforces a structured development process — like having a senior tech lead reviewing every step.

**Harness 框架**运行在 Claude Code 之上，强制执行结构化开发流程 —— 就像有一位高级技术负责人审查你的每一步。

---

## Quick Comparison / 快速对比

| Framework | Stars | One-Line Summary | Best For |
|-----------|-------|-----------------|----------|
| [Superpowers](superpowers/) | ~197k | Refuses to code until design is approved / 设计未批准就拒绝写代码 | TDD-driven projects / TDD 驱动的项目 |
| [ECC](ecc/) | ~100k+ | 28 agents + security scanner in one box / 28 个 Agent + 安全扫描一体 | Enterprise, security-critical / 企业级、安全敏感 |
| [GSD](gsd/) | ~60k | 6 commands, solves context rot / 6 个命令，解决上下文腐烂 | Quick start, small projects / 快速开始、小项目 |
| [Hermes](hermes-agent/) | ~140k | Agent that learns and improves itself / 自我学习和进化的 Agent | Long-term projects / 长期项目 |
| [GStack](gstack/) | ~83k | Virtual team: CEO to QA to Release / 虚拟团队：CEO 到 QA 到发布 | Solo devs wanting a team / 独立开发者 |
| [Spec-Kit](spec-kit/) | — | GitHub official, constitution-first / GitHub 官方，宪法优先 | Spec-heavy workflows / 规格驱动的工作流 |
| [BMAD](bmad-method/) | — | Agile sprints with AI agent roles / AI 角色跑敏捷冲刺 | Agile teams / 敏捷团队 |
| [Citadel](citadel/) | — | Parallel agents in isolated worktrees / 隔离工作树中并行 Agent | Large features, monorepos / 大功能、单仓库 |
| [CC Harness](claude-code-harness/) | — | Go guardrail engine blocks bad code / Go 防护引擎阻止坏代码 | Safety-first development / 安全优先开发 |
| [CC Workflows](claude-code-workflows/) | — | Auto-generates PRD + design before code / 写代码前自动生成 PRD + 设计文档 | Documentation-heavy projects / 文档驱动项目 |

---

## Which Framework Should I Use? / 我该用哪个框架？

### By Your Role / 按你的角色

| You are... / 你是... | Recommended / 推荐 | Why / 原因 |
|----------------------|-------------------|-----------|
| Complete beginner / 完全新手 | **GSD** | Lightest setup, 6 commands to learn / 最轻安装，只学 6 个命令 |
| Solo indie dev / 独立开发者 | **GStack** | Like having a full team for free / 免费拥有完整团队 |
| Startup founder / 创业者 | **GStack** or **Superpowers** | Ship fast with quality / 快速高质量交付 |
| Team lead / 团队负责人 | **Spec-Kit** or **BMAD** | Structure for the whole team / 为整个团队提供结构 |
| Enterprise dev / 企业开发者 | **ECC** | Security scanning + compliance / 安全扫描 + 合规 |
| Open source maintainer / 开源维护者 | **Superpowers** | TDD + spec ensures PR quality / TDD + 规格确保 PR 质量 |
| Researcher / 研究人员 | **Hermes Agent** | Self-improving, learns your patterns / 自进化，学习你的模式 |

### By Your Project / 按你的项目

| Project Type / 项目类型 | Recommended / 推荐 | Why / 原因 |
|------------------------|-------------------|-----------|
| Quick prototype (<1 day) / 快速原型 | **GSD** | Minimal overhead / 最小开销 |
| MVP (1-2 weeks) / 最小可行产品 | **GStack** or **Superpowers** | Structure without bureaucracy / 有结构无官僚 |
| Production app / 生产应用 | **ECC** or **CC Harness** | Security + guardrails / 安全 + 防护栏 |
| Large monorepo feature / 大型单仓功能 | **Citadel** | Parallel agents in worktrees / 工作树并行 Agent |
| API with docs / 带文档的 API | **CC Workflows** | Auto-generates PRD + design doc / 自动生成 PRD + 设计文档 |
| Agile sprint / 敏捷冲刺 | **BMAD-METHOD** | PM→Architect→Dev→QA roles / 敏捷角色 |
| Regulated industry / 受监管行业 | **Spec-Kit** + **ECC** | Constitution + security audit / 宪法 + 安全审计 |
| Long-running project / 长期项目 | **Hermes Agent** | Gets better over time / 随时间越来越好 |

### By What Bothers You / 按你的痛点

| Pain Point / 痛点 | Solution / 解决方案 |
|-------------------|-------------------|
| "AI forgets my requirements mid-session" / "AI 在会话中忘记需求" | **GSD** — fresh sub-agent per task / 每任务新建子 Agent |
| "AI writes code before understanding the problem" / "AI 不理解问题就写代码" | **Superpowers** — refuses to code until spec approved / 规格批准前拒绝写代码 |
| "Code has security holes I don't catch" / "代码有我发现不了的安全漏洞" | **ECC** — AgentShield with 1,282 security tests / 1282 项安全测试 |
| "I need to work on multiple parts simultaneously" / "需要同时开发多个部分" | **Citadel** — parallel agents in isolated worktrees / 隔离工作树并行 |
| "AI output looks generic and lifeless" / "AI 输出看起来模板化、无生气" | **GStack** — Designer role catches AI slop / 设计师角色捕捉 AI 水货 |
| "No documentation, just code" / "只有代码没有文档" | **CC Workflows** — auto-generates PRD, UI spec, design doc / 自动生成文档 |
| "Each sprint feels like starting over" / "每次冲刺都像从头开始" | **Hermes** — persistent memory + learned skills / 持久记忆 + 技能学习 |
| "Guardrails? What guardrails?" / "防护栏？什么防护栏？" | **CC Harness** — Go engine blocks bad code in <10ms / Go 引擎 <10ms 拦截坏代码 |

---

## Demo Config Checklist / 配置清单

What you need to set up each framework from scratch. Check off each step.

从零配置每个框架所需的步骤清单。

### Universal Prerequisites / 通用前置条件

All frameworks need these installed first:

所有框架都需要先安装以下内容：

```bash
# 1. Node.js 18+
#    Windows: download from https://nodejs.org
#    macOS:   brew install node
#    Linux:   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs

# 2. Claude Code CLI
npm install -g @anthropic-ai/claude-code
claude   # login with your Anthropic API key / 用 Anthropic API 密钥登录

# 3. Git
#    Windows: download from https://git-scm.com
#    macOS:   xcode-select --install
#    Linux:   sudo apt install git
```

### Per-Framework Setup / 各框架配置

#### Superpowers

```
□ Prerequisites installed / 前置条件已安装
□ Plugin: claude plugin add obra/superpowers
□ Verify: open Claude Code, type /brainstorm → should respond
□ Ready! Start with: /brainstorm <your feature idea>
  就绪！开始：/brainstorm <你的功能想法>

Config files created / 创建的配置文件:
  .claude/
  └── plugins/
      └── superpowers/        ← 14 skill files / 14 个技能文件
```

#### ECC (Everything Claude Code)

```
□ Prerequisites installed / 前置条件已安装
□ Install: npx ecc init
□ Select agents: npx ecc add agent:planning agent:tdd agent:security
□ Verify: open Claude Code, type /ecc-status → should list agents
□ Ready! Start with: /ecc-research <your task>
  就绪！开始：/ecc-research <你的任务>

Config files created / 创建的配置文件:
  .claude/
  ├── agents/               ← 28 agent definitions / 28 个 Agent 定义
  ├── skills/               ← 119 skill files / 119 个技能文件
  ├── commands/             ← 60 slash commands / 60 个斜杠命令
  └── hooks/                ← security hooks / 安全钩子
```

#### GSD (Get Shit Done)

```
□ Prerequisites installed / 前置条件已安装
□ Install: npx get-shit-done-cc
□ Init project: cd your-project && gsd init
□ Verify: /gsd-status → should show empty task board
□ Ready! Start with: /gsd-plan <your feature>
  就绪！开始：/gsd-plan <你的功能>

Config files created / 创建的配置文件:
  .claude/
  └── commands/             ← 6 slash commands / 6 个斜杠命令
  .gsd/
  ├── spec/                 ← specification files / 规格文件
  ├── tasks/                ← task tracking / 任务跟踪
  └── templates/            ← ~50 Markdown templates / 约 50 个模板
```

#### GStack

```
□ Prerequisites installed / 前置条件已安装
□ Clone: git clone https://github.com/garrytan/gstack.git
□ Copy:  cp -r gstack/commands/ your-project/.claude/commands/
         # Windows: Copy-Item -Recurse gstack\commands\ your-project\.claude\commands\
□ Verify: open Claude Code, type /ceo-review → should respond
□ Ready! Start with: /ceo-review <your feature idea>
  就绪！开始：/ceo-review <你的功能想法>

Config files created / 创建的配置文件:
  .claude/
  └── commands/             ← 23 skill files (one per role) / 23 个技能文件
```

#### Spec-Kit

```
□ Prerequisites installed / 前置条件已安装
□ Plugin: /plugin marketplace add github/spec-kit
□ Verify: type /speckit.constitution → should start constitution wizard
□ Ready! Start with: /speckit.constitution
  就绪！开始：/speckit.constitution

Config files created / 创建的配置文件:
  .claude/
  └── plugins/
      └── spec-kit/         ← 9 commands + SDD skill / 9 个命令 + SDD 技能
  .speckit/
  ├── constitution.yaml     ← project rules / 项目规则
  ├── specs/                ← requirement specs / 需求规格
  └── plans/                ← implementation plans / 实施计划
```

#### BMAD-METHOD

```
□ Prerequisites installed / 前置条件已安装
□ Install: npx bmad-method@next install
□ Follow installer prompts (select modules) / 按提示选择模块
□ Verify: open Claude Code, BMAD agents should be available
□ Ready! Start with: /bmad-pm <your product idea>
  就绪！开始：/bmad-pm <你的产品想法>

Config files created / 创建的配置文件:
  .claude/
  ├── agents/               ← PM, Architect, Developer, QA, DevOps
  ├── skills/               ← agile workflow skills / 敏捷工作流技能
  └── commands/             ← sprint commands / 冲刺命令
  .bmad/
  └── modules/              ← domain-specific modules / 领域专用模块
```

#### Hermes Agent

```
□ Prerequisites installed / 前置条件已安装
□ Claude Code plugin: claude plugin add hermes-ccc
□ (Or standalone: pip install hermes-agent)
□ Verify: type /hermes-status → should show skill inventory
□ Ready! Start with: /hermes <your task>
  就绪！开始：/hermes <你的任务>

Config files created / 创建的配置文件:
  .claude/
  └── plugins/
      └── hermes-ccc/       ← 46 native skills / 46 个原生技能
  .hermes/
  ├── memory/               ← persistent memory store / 持久记忆存储
  └── skills/               ← learned skills (grows over time) / 已学技能（随时间增长）
```

#### Citadel

```
□ Prerequisites installed / 前置条件已安装
□ Git 2.30+ required (worktree support) / 需要 Git 2.30+
□ Clone: git clone https://github.com/SethGammon/Citadel.git
□ Copy:  cp -r Citadel/.claude/ your-project/.claude/
□ Verify: type /do hello → should show tier routing
□ Ready! Start with: /do <your large feature>
  就绪！开始：/do <你的大功能>

Config files created / 创建的配置文件:
  .claude/
  ├── citadel/
  │   ├── skills/           ← 6 production skills / 6 个生产技能
  │   ├── campaigns/        ← persistent campaign state / 持久化任务状态
  │   └── config.yaml       ← tier routing + circuit breaker config / 路由 + 熔断配置
  └── hooks/                ← lifecycle hooks / 生命周期钩子
```

#### CC Harness

```
□ Prerequisites installed / 前置条件已安装
□ Go 1.21+ recommended (for guardrail engine) / 推荐 Go 1.21+
□ Clone: git clone https://github.com/Chachamaru127/claude-code-harness.git
□ Copy config to your project / 复制配置到你的项目
□ Verify: /harness setup → should create guardrail config
□ Ready! Start with: /harness plan <your feature>
  就绪！开始：/harness plan <你的功能>

Config files created / 创建的配置文件:
  .claude/
  └── harness/
      ├── skills/           ← 5 verb skills (setup/plan/work/review/release)
      ├── agents/           ← worker, reviewer, scaffolder
      ├── guardrails.yaml   ← rules engine config / 规则引擎配置
      └── hooks/            ← pre/post execution hooks / 执行前后钩子
```

#### CC Workflows

```
□ Prerequisites installed / 前置条件已安装
□ Plugin: /plugin marketplace add shinpr/claude-code-workflows
□ Verify: type /dev-workflows → should show available workflows
□ Ready! Start with: /dev-workflows <your feature idea>
  就绪！开始：/dev-workflows <你的功能想法>

Config files created / 创建的配置文件:
  .claude/
  └── plugins/
      └── dev-workflows/    ← workflow definitions / 工作流定义
  .workflows/
  ├── prd/                  ← generated PRDs / 生成的 PRD
  ├── design/               ← design documents / 设计文档
  ├── ui-specs/             ← UI specifications / UI 规格
  └── work-plans/           ← ordered task lists / 有序任务列表
```

---

## Detailed Feature Matrix / 详细功能矩阵

### Core Capabilities / 核心能力

| Feature / 功能 | Superpowers | ECC | GSD | GStack | Spec-Kit | BMAD | Hermes | Citadel | CC Harness | CC Workflows |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| TDD enforced / 强制 TDD | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Spec before code / 先规格后代码 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Sub-agent isolation / 子 Agent 隔离 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Security scanning / 安全扫描 | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Parallel agents / 并行 Agent | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Persistent memory / 持久记忆 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Self-improvement / 自我进化 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Guardrail engine / 防护引擎 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Auto-generate docs / 自动生成文档 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Multi-platform / 多平台支持 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Setup & Complexity / 安装与复杂度

| Aspect / 方面 | Superpowers | ECC | GSD | GStack | Spec-Kit | BMAD | Hermes | Citadel | CC Harness | CC Workflows |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Install time / 安装耗时 | 1 min | 3 min | 1 min | 2 min | 1 min | 2 min | 2 min | 3 min | 5 min | 1 min |
| Config files / 配置文件数 | ~14 | ~100+ | ~50 | ~23 | ~10 | ~20 | ~46 | ~10 | ~10 | ~5 |
| Learning curve / 学习曲线 | Medium | Hard | Easy | Easy | Medium | Medium | Medium | Hard | Medium | Medium |
| Dependencies / 依赖 | None | Node.js | Node.js | None | None | Node.js | Python | Git 2.30+ | Go 1.21+ | None |

### Workflow Comparison / 工作流对比

```
Superpowers:  Brainstorm → Spec → Plan → TDD → Subagent → Review → Finalize
              头脑风暴   → 规格 → 计划 → TDD → 子Agent  → 审查   → 完成

ECC:          Research → Plan → TDD → Security → Code Review → Build Fix
              调研     → 计划 → TDD → 安全扫描 → 代码审查   → 构建修复

GSD:          Init → Plan → Task (sub-agent) → Verify → Status → Finish
              初始化 → 计划 → 任务(子Agent) → 验证 → 状态 → 完成

GStack:       CEO → Eng Manager → Designer → Developer → Reviewer → QA → Security → Release
              CEO → 工程经理    → 设计师   → 开发者    → 审查员   → QA → 安全    → 发布

Spec-Kit:     Constitution → Specify → Clarify → Plan → Tasks → Implement
              宪法         → 规格    → 澄清   → 计划 → 任务  → 实现

BMAD:         PM (stories) → Architect (design) → Developer (code) → QA (test)
              PM(故事)     → 架构师(设计)       → 开发者(代码)    → QA(测试)

Hermes:       Execute → Evaluate → Learn → Improve (loop)
              执行    → 评估     → 学习  → 改进(循环)

Citadel:      /do → Tier Route → Campaign → Fleet (parallel) → Merge
              /do → 层级路由   → 战役     → 舰队(并行)       → 合并

CC Harness:   Setup → Plan → Work (parallel + guardrails) → Review → Release
              配置  → 计划 → 开发(并行+防护) → 审查 → 发布

CC Workflows: Analyze → PRD → UI Spec → Design Doc → Work Plan → Implement → Verify
              分析    → PRD → UI规格  → 设计文档   → 工作计划  → 实现     → 验证
```

---

## Framework Profiles / 框架详情

### [Superpowers](superpowers/) — TDD Discipline / TDD 纪律

> "I won't write code until you approve the design." / "设计不批准我就不写代码。"

- **Problem it solves**: AI jumps to coding before understanding the problem / AI 不理解问题就开始写代码
- **Key innovation**: Refuses premature coding + TDD + subagent isolation / 拒绝过早编码 + TDD + 子Agent隔离
- **Start command**: `/brainstorm <your idea>`
- **[→ Full Guide / 完整指南](superpowers/)**

### [ECC](ecc/) — Enterprise Arsenal / 企业军火库

> "28 agents, 119 skills, and a security scanner walk into your codebase." / "28 个 Agent、119 项技能和一个安全扫描器走进了你的代码库。"

- **Problem it solves**: Need comprehensive coverage across planning, coding, security, review / 需要全面覆盖规划、编码、安全、审查
- **Key innovation**: AgentShield security scanner + selective install architecture / AgentShield 安全扫描 + 按需安装
- **Start command**: `/ecc-research <your task>`
- **[→ Full Guide / 完整指南](ecc/)**

### [GSD](gsd/) — Lightweight Champion / 轻量冠军

> "6 commands. No dependencies. Just works." / "6 个命令。零依赖。开箱即用。"

- **Problem it solves**: Context rot — AI quality degrades in long sessions / 上下文腐烂 — 长会话中 AI 质量下降
- **Key innovation**: Fresh sub-agent context per task, built on native Claude Code features only / 每任务全新上下文，仅用 Claude Code 原生功能
- **Start command**: `/gsd-plan <your feature>`
- **[→ Full Guide / 完整指南](gsd/)**

### [GStack](gstack/) — Virtual Team / 虚拟团队

> "CEO, Designer, Eng Manager, QA, Security — all AI, all opinionated." / "CEO、设计师、工程经理、QA、安全 — 全是 AI，全有主见。"

- **Problem it solves**: Solo dev lacks diverse perspectives (design, security, QA) / 独立开发者缺乏多元视角
- **Key innovation**: Opinionated role-based reviews — Designer catches AI slop, Security runs OWASP / 有主见的角色审查
- **Start command**: `/ceo-review <your idea>`
- **[→ Full Guide / 完整指南](gstack/)**

### [Spec-Kit](spec-kit/) — Blueprint First / 蓝图优先

> "No blueprints, no building." / "没有蓝图，就不施工。"

- **Problem it solves**: AI coding without clear requirements leads to rework / AI 在需求不明时编码导致返工
- **Key innovation**: Constitution defines non-negotiable rules before any code / 宪法在任何代码之前定义不可违反的规则
- **Start command**: `/speckit.constitution`
- **[→ Full Guide / 完整指南](spec-kit/)**

### [BMAD-METHOD](bmad-method/) — Agile AI Team / 敏捷 AI 团队

> "A full agile sprint with AI teammates." / "和 AI 队友一起跑完整的敏捷冲刺。"

- **Problem it solves**: Need agile process but team is just you and AI / 需要敏捷流程但团队只有你和 AI
- **Key innovation**: Each AI agent plays a real agile role (PM, Architect, Dev, QA) / 每个 AI Agent 扮演真实敏捷角色
- **Start command**: `/bmad-pm <your product idea>`
- **[→ Full Guide / 完整指南](bmad-method/)**

### [Hermes Agent](hermes-agent/) — Self-Evolving / 自进化

> "An intern that gets better every day and never forgets." / "一个每天进步且永不遗忘的实习生。"

- **Problem it solves**: Starting over with each session, no learning retention / 每次会话从头开始，不保留学习
- **Key innovation**: Self-improving skills + persistent memory across sessions / 自进化技能 + 跨会话持久记忆
- **Start command**: `/hermes <your task>`
- **[→ Full Guide / 完整指南](hermes-agent/)**

### [Citadel](citadel/) — Parallel Fleet / 并行舰队

> "3 agents, 3 worktrees, 3x speed." / "3 个 Agent，3 个工作树，3 倍速度。"

- **Problem it solves**: Large features take too long sequentially / 大功能按顺序开发太慢
- **Key innovation**: Fleet mode — parallel agents in isolated git worktrees + discovery relay / 舰队模式 — 隔离工作树并行 + 发现中继
- **Start command**: `/do <your large feature>`
- **[→ Full Guide / 完整指南](citadel/)**

### [CC Harness](claude-code-harness/) — Guardrailed / 有防护的

> "Same speed, much safer." / "同样的速度，安全得多。"

- **Problem it solves**: AI writes dangerous code (hardcoded secrets, SQL injection) / AI 写出危险代码
- **Key innovation**: Go-native guardrail engine blocks bad patterns in <10ms / Go 防护引擎 <10ms 拦截危险模式
- **Start command**: `/harness plan <your feature>`
- **[→ Full Guide / 完整指南](claude-code-harness/)**

### [CC Workflows](claude-code-workflows/) — Docs-First / 文档优先

> "PRD and design doc before the first line of code." / "第一行代码之前先有 PRD 和设计文档。"

- **Problem it solves**: Code exists but no one knows why it was built that way / 代码存在但没人知道为什么这样写
- **Key innovation**: Auto-generates PRD → UI spec → Design doc → Work plan before coding / 编码前自动生成完整文档链
- **Start command**: `/dev-workflows <your idea>`
- **[→ Full Guide / 完整指南](claude-code-workflows/)**

---

## Learning Path / 学习路径

```
Week 1: Pick ONE, learn it well / 第一周：选一个，学透它
├── Never used AI coding?    → GSD (simplest)
│   从未用过 AI 编码？         → GSD（最简单）
├── Want a team experience?  → GStack (most fun)
│   想要团队体验？             → GStack（最有趣）
└── Want strict process?     → Superpowers (most disciplined)
    想要严格流程？              → Superpowers（最有纪律）

Week 2-3: Add a second layer / 第二三周：加一层
├── Add security scanning    → ECC AgentShield
│   加安全扫描                 → ECC AgentShield
├── Add parallel execution   → Citadel
│   加并行执行                 → Citadel
└── Add persistent learning  → Hermes Agent
    加持久学习                  → Hermes Agent

Week 4+: Combine for your ideal workflow / 第四周+：组合你的理想工作流
└── Example: GSD (tasks) + GStack (reviews) + ECC (security)
    示例：GSD（任务管理）+ GStack（角色审查）+ ECC（安全扫描）
```

---

## Each Directory Contains / 每个目录包含

| File / 文件 | Purpose / 用途 |
|-------------|---------------|
| `README.md` | Full guide: intro + setup (Win/Mac/Linux) + walkthrough + troubleshooting / 完整指南 |
| `example_workflow.py` | Workflow simulation you can run locally / 可本地运行的工作流模拟 |
| `test_*.py` | Tests without API keys / 无需 API 密钥的测试 |

```bash
# Run any example / 运行示例
cd examples/frameworks/<framework>
python example_workflow.py

# Run tests / 运行测试
pytest test_*.py -v
```

---

<a id="中文版导航"></a>

## 中文版导航

> **[English](#table-of-contents)** | 中文

### 快速选择

| 我的情况 | 推荐框架 | 第一个命令 |
|---------|---------|----------|
| 完全新手，想最快上手 | [GSD](gsd/) | `/gsd-plan <功能描述>` |
| 独立开发者，想要团队感 | [GStack](gstack/) | `/ceo-review <想法>` |
| 注重代码质量和测试 | [Superpowers](superpowers/) | `/brainstorm <想法>` |
| 企业开发，注重安全 | [ECC](ecc/) | `/ecc-research <任务>` |
| 需要完整文档链 | [CC Workflows](claude-code-workflows/) | `/dev-workflows <想法>` |
| 团队用敏捷流程 | [BMAD-METHOD](bmad-method/) | `/bmad-pm <产品想法>` |
| 需要规格驱动 | [Spec-Kit](spec-kit/) | `/speckit.constitution` |
| 大功能要并行开发 | [Citadel](citadel/) | `/do <大功能描述>` |
| 想要 AI 越用越聪明 | [Hermes Agent](hermes-agent/) | `/hermes <任务>` |
| 需要防护栏防错 | [CC Harness](claude-code-harness/) | `/harness plan <功能>` |

### 框架分类

- **方法论框架**（怎么做）：[Superpowers](superpowers/) · [GSD](gsd/) · [Spec-Kit](spec-kit/) · [BMAD](bmad-method/)
- **虚拟团队框架**（谁来做）：[GStack](gstack/) · [ECC](ecc/)
- **编排进化框架**（做得更好）：[Hermes Agent](hermes-agent/) · [Citadel](citadel/)
- **全生命周期框架**（全流程）：[CC Harness](claude-code-harness/) · [CC Workflows](claude-code-workflows/)

### 所有框架详情

每个框架目录都包含完整的中英双语指南：安装步骤（Windows/macOS/Linux）、实操演示、常见问题排查。

点击上方任意框架名称进入详情页。

---

<p align="center">
  <sub>Part of <a href="../../README.md">claude-engineer</a> — contributions welcome! / 欢迎贡献！</sub>
</p>
