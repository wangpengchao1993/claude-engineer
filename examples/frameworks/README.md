# AI Coding Workflow Frameworks — From Idea to Shipped Code
# AI 编码工作流框架 — 从想法到交付代码

> A beginner-friendly, bilingual guide to the most popular Claude Code harness frameworks in 2026.
> These frameworks transform AI coding from "chatting with a bot" into structured engineering workflows.
>
> 面向小白的双语指南：2026 年最热门的 Claude Code 工作流框架。
> 这些框架将 AI 编码从"和机器人聊天"变成结构化的工程流程。

---

## What is a Harness Framework? / 什么是 Harness 框架？

A harness framework sits **on top of** Claude Code (or other AI coding tools) and enforces a disciplined development process:

Harness 框架运行在 Claude Code（或其他 AI 编码工具）**之上**，强制执行规范的开发流程：

```
Without Harness / 没有 Harness:
  "Build me a login page" → AI writes code → Maybe works, maybe not
  "帮我做个登录页" → AI 写代码 → 也许能用，也许不行

With Harness / 有 Harness:
  Idea → Requirements → Design → Plan → TDD → Implementation → Review → Ship
  想法 → 需求 → 设计 → 计划 → 测试驱动 → 实现 → 审查 → 交付
```

---

## Framework Overview / 框架总览

### Methodology Frameworks / 方法论框架

| Framework / 框架 | Stars | Core Approach / 核心方法 | Difficulty / 难度 |
|------------------|-------|------------------------|-------------------|
| [Superpowers](superpowers/) | ~197k | 7-phase TDD workflow: brainstorm→spec→plan→TDD→subagent / 7 阶段 TDD 流程 | Medium / 中等 |
| [GSD](gsd/) | ~60k | Lightweight 6-command loop, solves context rot / 轻量 6 命令循环，解决上下文腐烂 | Easy / 简单 |
| [Spec-Kit](spec-kit/) | — | GitHub official, spec-driven: constitution→specify→plan→implement / GitHub 官方规格驱动 | Medium / 中等 |
| [BMAD-METHOD](bmad-method/) | — | Agile multi-role: PM→Architect→Developer→QA / 敏捷多角色团队 | Medium / 中等 |

### Virtual Team Frameworks / 虚拟团队框架

| Framework / 框架 | Stars | Core Approach / 核心方法 | Difficulty / 难度 |
|------------------|-------|------------------------|-------------------|
| [GStack](gstack/) | ~83k | YC CEO's 23-skill virtual team: CEO→Designer→Eng→QA→Security / YC CEO 的虚拟工程团队 | Easy / 简单 |
| [ECC](ecc/) | ~100k+ | All-in-one: 28 agents + 119 skills + security scanner / 全能型 28 Agent 工具集 | Hard / 较难 |

### Orchestration & Evolution / 编排与进化框架

| Framework / 框架 | Stars | Core Approach / 核心方法 | Difficulty / 难度 |
|------------------|-------|------------------------|-------------------|
| [Hermes Agent](hermes-agent/) | ~140k | Self-evolving agent with persistent memory / 自进化 Agent + 持久记忆 | Medium / 中等 |
| [Citadel](citadel/) | — | Parallel agents in isolated worktrees + campaign persistence / 并行 Agent + 跨会话持久化 | Hard / 较难 |

### Full-Lifecycle Workflows / 全生命周期工作流

| Framework / 框架 | Stars | Core Approach / 核心方法 | Difficulty / 难度 |
|------------------|-------|------------------------|-------------------|
| [CC Harness](claude-code-harness/) | — | Plan→Work→Review cycle with Go guardrail engine / 计划→开发→审查 + Go 引擎防护 | Medium / 中等 |
| [CC Workflows](claude-code-workflows/) | — | Full lifecycle: idea→PRD→design→implement→verify / 全链路：想法→PRD→设计→实现→验证 | Medium / 中等 |

---

## How They Compare / 框架对比

### "I want to..." / "我想要..."

| Goal / 目标 | Best Pick / 推荐 | Why / 原因 |
|-------------|-----------------|-----------|
| Start with structure, minimal setup / 最轻量起步 | GSD | Only 6 commands, no dependencies / 只有 6 个命令 |
| Enforce TDD discipline / 强制 TDD 纪律 | Superpowers | Refuses to code before spec + TDD / 不批准就不写代码 |
| Simulate a full team / 模拟完整团队 | GStack | 7 roles from CEO to Release Engineer / 7 个角色 |
| Maximum coverage / 最大覆盖 | ECC | 28 agents, 119 skills, security scanner / 最全面 |
| GitHub-official approach / GitHub 官方方案 | Spec-Kit | Constitution-driven, by GitHub / 宪法驱动 |
| Agile sprints with AI / 用 AI 跑敏捷冲刺 | BMAD-METHOD | PM→Architect→Dev→QA roles / 敏捷角色 |
| Agent that learns / Agent 能自我学习 | Hermes Agent | Self-improving skills + memory / 自进化 |
| Parallel development / 并行开发 | Citadel | Fleet mode, isolated worktrees / 舰队模式 |
| Guardrails to prevent mistakes / 防护栏防止错误 | CC Harness | Go engine, sub-10ms checks / Go 引擎实时检查 |
| Full docs + code pipeline / 完整文档+代码流水线 | CC Workflows | Generates PRD, design doc, then code / 先文档后代码 |

---

## Learning Path / 学习路径

```
Stage 1: Pick One and Start / 选一个开始
├── Beginner → GSD (lightest) or GStack (most fun)
│   小白 → GSD（最轻量）或 GStack（最有趣）
└── Experienced → Superpowers (most disciplined) or Spec-Kit (most structured)
    有经验 → Superpowers（最有纪律）或 Spec-Kit（最有结构）

Stage 2: Add Depth / 深入
├── Add security → ECC's AgentShield
│   加安全 → ECC 的 AgentShield
├── Add parallel execution → Citadel
│   加并行 → Citadel
└── Add self-improvement → Hermes Agent
    加自进化 → Hermes Agent

Stage 3: Combine / 组合使用
└── Mix frameworks for your ideal workflow
    组合多个框架打造你的理想工作流
```

---

## Each Directory Contains / 每个目录包含

| File / 文件 | Purpose / 用途 |
|-------------|---------------|
| `README.md` | Framework introduction, workflow, comparisons / 框架介绍、流程、对比 |
| `example_workflow.py` | Workflow simulation with bilingual comments / 工作流模拟（双语注释） |
| `test_*.py` | Tests that work without API keys / 无需 API 密钥的测试 |

```bash
# Run any example / 运行任意示例
cd examples/frameworks/<framework>
python example_workflow.py

# Run tests / 运行测试
pytest test_*.py -v
```

---

<p align="center">
  <sub>Part of <a href="../../README.md">claude-engineer</a> — contributions welcome! / 欢迎贡献！</sub>
</p>
