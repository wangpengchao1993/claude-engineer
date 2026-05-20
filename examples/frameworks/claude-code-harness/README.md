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

*Harness does not replace Claude Code — it makes Claude Code safer and more structured.*

*Harness 不是替代 Claude Code -- 它让 Claude Code 更安全、更有结构。*
