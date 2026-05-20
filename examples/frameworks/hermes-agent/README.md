# Hermes Agent — The Self-Evolving AI Agent / 自进化 AI 智能体

> **~140k GitHub Stars** | By [Nous Research](https://nousresearch.com) | Open Source
>
> **~14万 GitHub Stars** | 由 [Nous Research](https://nousresearch.com) 开发 | 开源

---

## What is Hermes Agent? / 什么是 Hermes Agent？

Hermes Agent is an AI agent that **learns and improves from every interaction**.
Unlike other frameworks where skills are static and hand-coded, Hermes **evolves**.

Hermes Agent 是一个**从每次交互中学习和改进**的 AI 智能体。
不同于其他技能固定、手动编写的框架，Hermes 会**自我进化**。

Think of it as **"an intern that gets better every day and never forgets what it learned."**

可以把它想象成**"一个每天都在进步、永远不会忘记所学知识的实习生。"**

Launched in February 2026, Hermes hit 140k stars in under 3 months and became
the #1 most-used AI agent on OpenRouter (224B tokens/day).

Hermes 于 2026 年 2 月发布，不到 3 个月即获得 14 万 stars，成为 OpenRouter 上
使用量最大的 AI 智能体（每日 2240 亿 tokens）。

---

## Core Differentiator / 核心差异化优势

Three pillars make Hermes unique:

三大支柱使 Hermes 与众不同：

1. **Self-Improving Skills / 自改进技能** — Skills get better each time they are used.
   技能在每次使用后都会变得更好。

2. **Persistent Memory / 持久记忆** — Context and knowledge carry across sessions.
   上下文和知识跨会话保留。

3. **Closed Learning Loop / 闭环学习** — Do, evaluate, learn, improve. Automatically.
   执行、评估、学习、改进，全自动。

---

## How It Learns / 学习原理

```
Task Execution  ──>  Evaluate Results  ──>  Update Skills  ──>  Better Next Time
  执行任务      ──>    评估结果        ──>    更新技能     ──>    下次做得更好
```

Each time Hermes completes a task, it:

每次 Hermes 完成任务时，它会：

1. **Execute** the task using its current skills / 用当前技能**执行**任务
2. **Evaluate** the outcome (Did it work? How well?) / **评估**结果（成功了吗？效果如何？）
3. **Extract patterns** from successes and failures / 从成功和失败中**提取模式**
4. **Update skills** so the next run is better / **更新技能**使下次执行更好

---

## Integration with Claude Code / 与 Claude Code 的集成

Hermes can **delegate coding tasks** to Claude Code via the terminal.
When Hermes needs to write code, edit files, or manage git, it hands off to Claude Code.

Hermes 可以通过终端**将编码任务委派**给 Claude Code。
当 Hermes 需要编写代码、编辑文件或管理 git 时，它会交给 Claude Code 处理。

### hermes-CCC — The Native Claude Code Port / 原生 Claude Code 移植版

**hermes-CCC** is the native port that runs entirely inside Claude Code:

**hermes-CCC** 是完全在 Claude Code 内部运行的原生移植版：

- **46 native skills** built for Claude Code / 为 Claude Code 构建的 **46 个原生技能**
- **No OAuth required** — works immediately / **无需 OAuth** — 开箱即用
- Runs as a Claude Code plugin / 作为 Claude Code 插件运行

---

## Key Features / 主要特性

| Feature / 特性 | Description / 描述 |
|---|---|
| **Persistent Memory** / 持久记忆 | Remembers context across sessions / 跨会话记忆上下文 |
| **Skill Marketplace** / 技能市场 | Share and download community skills / 分享和下载社区技能 |
| **Model-Agnostic** / 模型无关 | Works with any LLM backend / 兼容任何 LLM 后端 |
| **Self-Improving** / 自我改进 | Skills evolve with use / 技能随使用而进化 |

---

## Installation / 安装

### Option 1: Standalone / 独立安装

```bash
pip install hermes-agent
hermes init
```

### Option 2: Claude Code Plugin (hermes-CCC) / Claude Code 插件

```bash
claude install hermes-ccc
```

That's it — 46 skills are immediately available inside Claude Code.

就这么简单 — 46 个技能立即在 Claude Code 中可用。

---

## Hermes vs Superpowers / Hermes 与 Superpowers 对比

| Aspect / 方面 | Hermes Agent | Superpowers |
|---|---|---|
| **Skills** / 技能 | Self-evolving / 自进化 | Static methodology / 静态方法论 |
| **Learning** / 学习 | Automatic from usage / 自动从使用中学习 | Manual configuration / 手动配置 |
| **Memory** / 记忆 | Persistent across sessions / 跨会话持久 | Per-session / 每次会话 |
| **Approach** / 方式 | Adaptive agent / 自适应智能体 | Structured workflow / 结构化工作流 |

Both are excellent tools — Hermes excels when you want an agent that gets smarter over time,
while Superpowers excels at providing a consistent, structured development methodology.

两者都是优秀工具 — 当你想要一个随时间变聪明的智能体时 Hermes 更佳，
而 Superpowers 在提供一致的结构化开发方法论方面更强。

---

## Learn More / 了解更多

- GitHub: [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Documentation / 文档: [docs.hermes-agent.ai](https://docs.hermes-agent.ai)
- Skill Marketplace / 技能市场: [skills.hermes-agent.ai](https://skills.hermes-agent.ai)
